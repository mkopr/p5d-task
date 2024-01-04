import json

import pytest
from lxml import html

from app.parsers import HTMLParsingStrategy, JSONParsingStrategy
from app.schemas import ParsedData
from tests.mock_data_helpers import read_mock_data


class TestHTMLParsingStrategy:
    mock_html_content = read_mock_data("html", "dummy_page.html")

    def test_parse_empty_html(self):
        parser = HTMLParsingStrategy()
        result = parser.parse(None)
        assert result.extracted_param is None

    def test_parse_correct_html(self):
        parser = HTMLParsingStrategy()
        result = parser.parse(self.mock_html_content)
        parsed_data = ParsedData(extracted_param="desiredValue")
        assert result.extracted_param == parsed_data.extracted_param

    def test_extract_href_attribute_success(self):
        parser = HTMLParsingStrategy()
        test_html = '<a href="http://example.com?key=value">Link</a>'
        tree = html.fromstring(test_html)
        href = parser.extract_href_attribute(tree, "//a/@href")
        assert href == "http://example.com?key=value"

    def test_extract_href_attribute_failure(self):
        parser = HTMLParsingStrategy()
        test_html = "<a>Missing href</a>"
        tree = html.fromstring(test_html)
        href = parser.extract_href_attribute(tree, "//a/@href")
        assert href is None

    def test_parse_url_query_parameter_success(self):
        parser = HTMLParsingStrategy()
        url = "http://example.com?key=value"
        param = parser.parse_url_query_parameter(url, "key")
        assert param == "value"

    def test_parse_url_query_parameter_failure(self):
        parser = HTMLParsingStrategy()
        url = "http://example.com"
        param = parser.parse_url_query_parameter(url, "key")
        assert param is None


class TestJSONParsingStrategy:
    mock_json_content = read_mock_data("json", "dummy_api.json")

    def test_parse_valid_json_string(self):
        parser = JSONParsingStrategy()
        result = parser.parse(self.mock_json_content)
        assert isinstance(result, ParsedData)
        assert result.project_info.hash == "project123hash"

    def test_parse_valid_json_dict(self):
        parser = JSONParsingStrategy()
        result = parser.parse(self.mock_json_content)
        assert isinstance(result, ParsedData)
        assert result.project_info.name == "Project ABC"

    def test_parse_invalid_data_type(self):
        parser = JSONParsingStrategy()
        with pytest.raises(TypeError):
            parser.parse(123)

    def test_correct_floor_and_room_counts(self):
        parser = JSONParsingStrategy()
        result = parser.parse(self.mock_json_content)
        assert result.project_info.floor_count == 2
        assert result.project_info.room_count == 5

    def test_find_items_by_class_name(self):
        parser = JSONParsingStrategy()
        items = json.loads(self.mock_json_content)["items"][0]["data"]["items"]
        floors = parser.find_items_by_class(items, "Floor")
        assert len(floors) == 2

    def test_count_nested_items_by_class_name(self):
        parser = JSONParsingStrategy()
        items = json.loads(self.mock_json_content)["items"][0]["data"]["items"]
        room_count = parser.count_nested_items_by_class(items, "Room")
        assert room_count == 5
