from abc import ABC, abstractmethod
from typing import Any, Dict, Union

import aiohttp

from app.logger import logger


class AsyncDataFetcher(ABC):
    """
    Abstract base class for data fetching operations.

    Defines a template method to fetch data from a URL.
    """

    @abstractmethod
    async def fetch_data(
        self, url: str, session: aiohttp.ClientSession
    ) -> Union[Dict[str, Any], str, None]:
        """
        Fetch data from a given URL.

        :param url: The URL to fetch data from.
        :param session: The aiohttp ClientSession to use for fetching data.
        :return: The fetched data in a structured format, or None if fetching fails.
        """
        pass


class AsyncHTMLDataFetcher(AsyncDataFetcher):
    """
    Fetcher for retrieving HTML content from a URL.

    Extends the DataFetcher abstract base class.
    """

    async def fetch_data(
        self, url: str, session: aiohttp.ClientSession
    ) -> Union[Dict[str, Any], str, None]:
        """
        Fetch HTML data from a URL using an existing aiohttp.ClientSession.

        :param url: The URL to fetch HTML content from.
        :param session: The aiohttp ClientSession to use for fetching data.
        :return: The HTML content as a string, or None if fetching fails.
        """
        logger.info(f"Fetching html data from {url}")
        try:
            async with session.get(url) as response:
                return await response.text()
        except (aiohttp.ClientResponseError, aiohttp.InvalidURL) as e:
            logger.error(f"Error fetching HTML data: {e}")
            return None


class AsyncJSONDataFetcher(AsyncDataFetcher):
    """
    Fetcher for retrieving JSON content from a URL.

    Extends the DataFetcher abstract base class.
    """

    async def fetch_data(
        self, url: str, session: aiohttp.ClientSession
    ) -> Union[Dict[str, Any], str, None]:
        """
        Fetch JSON data from a URL.

        :param url: The URL to fetch JSON content from.
        :param session: The aiohttp ClientSession to use for fetching data.
        :return: A dictionary representing the JSON data, or None if fetching fails.
        """
        logger.info(f"Fetching json data from {url}")
        try:
            async with session.get(url) as response:
                return await response.json()
        except (aiohttp.ClientResponseError, aiohttp.InvalidURL) as e:
            logger.error(f"Error fetching JSON data: {e}")
            return None
