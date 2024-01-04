import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse

from lxml import etree, html

from app.config import PROJECT_ID_XPATH
from app.logger import logger
from app.schemas import ParsedData, ProjectInfo


class ParsingStrategy(ABC):
    """
    Abstract base class defining a parsing strategy interface.

    Provides a template method 'parse' to be implemented by concrete subclasses.
    """

    @abstractmethod
    def parse(self, data: str) -> ParsedData:
        """
        Parse given data and return structured information.

        :param data: The data to be parsed as a string.
        :return: ParseData object containing the parsed data.
        """
        pass


class JSONParsingStrategy(ParsingStrategy):
    """
    Strategy for parsing JSON data, specifically tailored for project-related content.
    Implements methods for counting floors and rooms in a given JSON structure.
    """

    def parse(self, data: Union[str, Dict[str, Any]]) -> ParsedData:
        """
        Parse JSON data to count floors and rooms.

        :param data: The JSON data as a string or dictionary.
        :return: ParseData object containing the parsed data.
        """
        match data:
            case str():
                json_data = json.loads(data)
            case dict():
                json_data = data
            case _:
                logger.error(f"Invalid data type: {type(data)}, {data}")
                raise TypeError("Invalid data type. Expected str or dict.")

        floor_count, room_count = self.get_floor_and_room_counts(
            json_data, "Floor", "Room"
        )

        project_hash = self.get_item_field(json_data, "hash")
        project_title = self.get_item_field(json_data, "name")

        project_info = ProjectInfo(
            hash=project_hash,
            name=project_title,
            floor_count=floor_count,
            room_count=room_count,
        )

        return ParsedData(project_info=project_info)

    @staticmethod
    def get_item_field(data: Dict[str, Any], field_name: str) -> str:
        """
        Get a specific field value from project items object.

        :param data: The JSON data as a dictionary.
        :param field_name: The name of the field to retrieve ('hash' or 'title').
        :return: The value of the specified field as a string.
        """
        return data.get("items", [{}])[0].get(field_name)

    @staticmethod
    def find_items_by_class(
        items: List[Dict[str, Any]], target_class_name: str
    ) -> List[Dict[str, Any]]:
        """
        Filter items by class name.

        :param items: A list of dictionary items.
        :param target_class_name: The target class name to filter by.
        :return: Filtered list of items.
        """
        return [
            item
            for item in items
            if item.get("className") == target_class_name
        ]

    def get_floor_and_room_counts(
        self, data: Dict[str, Any], floor_class_name: str, room_class_name: str
    ) -> Tuple[int, int]:
        """
        Analyzes and counts the number of floors and rooms in the project data.

        :param data: The JSON data from the API response.
        :param floor_class_name: The class name representing floors.
        :param room_class_name: The class name representing rooms.
        :return: A dictionary with the count of floors and the total number of rooms.
        """
        total_floors = 0
        total_rooms = 0

        for project_section in data.get("items", []):
            try:
                items = project_section.get("data", {}).get("items", [])
            except AttributeError:  # sometimes data is JSON string
                items = json.loads(project_section.get("data", {})).get(
                    "items", []
                )

            floors = self.find_items_by_class(
                items,
                floor_class_name,
            )
            total_floors += len(floors)
            total_rooms += self.count_nested_items_by_class(
                floors, room_class_name
            )

        return total_floors, total_rooms

    def count_nested_items_by_class(
        self, parent_items: List[Dict[str, Any]], nested_class_name: str
    ) -> int:
        """
        Counts the total number of nested items that match a specified class name.

        :param parent_items: A list of parent items containing nested items.
        :param nested_class_name: The class name of nested items to be counted.
        :return: The total count of nested items matching the specified class name.
        """
        return sum(
            len(
                self.find_items_by_class(
                    item.get("items", []), nested_class_name
                )
            )
            for item in parent_items
        )


class HTMLParsingStrategy(ParsingStrategy):
    """
    Strategy for parsing HTML content, focused on extracting specific attributes like href.

    Implements a method to extract href attribute using XPath.
    """

    def parse(self, data: Optional[str]) -> ParsedData:
        """
        Parse HTML data to extract param form href attribute url.

        :param data: The HTML data as a string.
        :return: A ParsedData object containing the extracted param value.
        """
        if not data:
            logger.error("Empty HTML data")
            return ParsedData(extracted_param=None)

        tree = html.fromstring(data)
        href = self.extract_href_attribute(tree, PROJECT_ID_XPATH)
        if not href:
            logger.error("Could not extract href attribute from HTML data")
            return ParsedData(extracted_param=None)

        param_value_from_url = self.parse_url_query_parameter(href, "key")
        if not param_value_from_url:
            logger.error(f"Could not extract param value from URL: {href}")

        return ParsedData(extracted_param=param_value_from_url)

    @staticmethod
    def extract_href_attribute(
        tree: etree._Element, xpath: str
    ) -> Optional[str]:
        """
        Extract the href attribute from the given element tree using XPath.

        :param tree: The element tree to search.
        :param xpath: The XPath query string.
        :return: The extracted href attribute value, or None if not found.
        """
        href_elements = tree.xpath(xpath)
        return href_elements[0] if href_elements else None

    @staticmethod
    def parse_url_query_parameter(url: str, parameter: str) -> Optional[str]:
        """
        Parses a URL and extracts the value of a specified query parameter.

        :param url: The URL to parse.
        :param parameter: The name of the query parameter to extract.
        :return: The value of the query parameter if found, otherwise None.
        """
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        return params.get(parameter, [None])[0]
