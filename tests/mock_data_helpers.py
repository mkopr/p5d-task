import asyncio
import os
from typing import Any, Callable, Union

from aiohttp import ClientSession

# Global variables to track concurrent tasks
concurrent_tasks: int = 0
max_concurrent_reached: bool = False
max_concurrent_tasks: int = 2


async def mock_fetch_and_parse(
    sem: asyncio.Semaphore, url: str, session: ClientSession, csv_handler: Any
) -> None:
    """
    Mock function to simulate fetching and parsing data.

    Simulates asynchronous operations and tracks the number of concurrent tasks
    to verify that it does not exceed the specified maximum.

    :param sem: Semaphore to control concurrency.
    :param url: URL to fetch data from (not used in mock).
    :param session: Client session for HTTP requests (not used in mock).
    :param csv_handler: CSV handler for data processing (not used in mock).
    """
    global concurrent_tasks, max_concurrent_reached
    async with sem:  # Respect the semaphore limit
        concurrent_tasks += 1
        if concurrent_tasks > max_concurrent_tasks:
            max_concurrent_reached = True
        await asyncio.sleep(0.1)  # Simulate async operation
        concurrent_tasks -= 1


def get_mock_data_file_path(data_type: str, file_name: str) -> str:
    """
    Constructs the file path for mock data.

    :param data_type: Type of mock data ('html' or 'json').
    :param file_name: Name of the file containing mock data.
    :return: Full file path of the mock data file.
    """
    valid_types = ["html", "json", "csv"]
    if data_type not in valid_types:
        raise ValueError(f"data_type must be one of {valid_types}")

    return os.path.join(
        os.path.dirname(__file__), "mocks", data_type, file_name
    )


def read_mock_data(data_type: str, file_name: str) -> str:
    """
    Reads mock data from a specified file. Constructs the file path using `get_mock_data_file_path`
    and then reads the content from that file.

    :param data_type: Type of mock data ('html' or 'json').
    :param file_name: Name of the file containing mock data.
    :return: Content of the mock data file as a string.
    """
    file_path = get_mock_data_file_path(data_type, file_name)
    with open(file_path, "r") as file:
        return file.read()


class MockResponse:
    """
    Mock response class for simulating aiohttp response.

    This class mimics the behavior of an aiohttp response object, particularly
    supporting the asynchronous context manager protocol and 'json' and `text` coroutine methods.

    :param content: The content to be returned by the `text` or `json` method.
    """

    def __init__(self, content: Union[str, dict, list]):
        self.content = content

    async def __aenter__(self) -> "MockResponse":
        """
        Enter the runtime context related to this object.

        :return: An instance of MockResponse.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the runtime context and perform any cleanup actions.

        :param exc_type: The exception type if an exception has occurred.
        :param exc_val: The exception value if an exception has occurred.
        :param exc_tb: The exception traceback if an exception has occurred.
        """
        pass

    async def text(self) -> Any:
        """
        Simulate the text method of the aiohttp response object.

        :return: The mock content as a string.
        """
        return self.content

    async def json(self) -> Any:
        """
        Simulate the json method of the aiohttp response object.

        :return: The mock content as a JSON object.
        """
        return self.content


def mock_get(content: Union[str, dict, list]) -> Callable:
    """
    Create a mock get function for aiohttp.ClientSession.

    This function returns a callable that simulates the 'get' method of
    aiohttp.ClientSession. When called, it returns an instance of MockResponse
    initialized with the provided content and content type.

    :param content: The content to be returned by the mock response. Can be a string (for HTML) or a dict/list (for JSON).
    :return: A function simulating aiohttp.ClientSession.get.
    """

    def _mock_get(*args, **kwargs) -> MockResponse:
        return MockResponse(content)

    return _mock_get
