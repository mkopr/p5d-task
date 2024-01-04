import asyncio
from unittest.mock import MagicMock

import pytest

from app.csv_handler import CSVHandler
from app.fetchers import AsyncHTMLDataFetcher, AsyncJSONDataFetcher
from app.parsers import HTMLParsingStrategy, JSONParsingStrategy
from app.schemas import ParsedData, ProjectInfo
from app.utils import (
    fetch_and_parse_project_data_to_csv,
    fetch_data_and_save_in_parallel,
    is_valid_url,
)
from tests.mock_data_helpers import (
    max_concurrent_tasks,
    mock_fetch_and_parse,
    read_mock_data,
)

# Preparing mock data
mock_html_content = read_mock_data("html", "dummy_page.html")
mock_json_content = read_mock_data("json", "dummy_api.json")


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://planner5d.com/",
        "ftp://myserver.net",
        "http://localhost:8000",
    ],
)
def test_is_valid_url_with_valid_urls(url):
    assert is_valid_url(url)


@pytest.mark.parametrize(
    "url", ["example", "http://", "www.google.com", "12345", "http//com", ""]
)
def test_is_valid_url_with_invalid_urls(url):
    assert not is_valid_url(url)


@pytest.mark.asyncio
async def test_max_concurrent_tasks(mocker):
    """
    Test to verify that the maximum number of concurrent tasks in
    fetch_data_and_save_in_parallel function does not exceed the specified limit.
    """
    mock_urls = [
        "http://example.com/1",
        "http://example.com/2",
        "http://example.com/3",
    ]

    # Reset global variables before each test
    global concurrent_tasks, max_concurrent_reached
    concurrent_tasks = 0
    max_concurrent_reached = False

    mocker.patch("app.utils.aiohttp.ClientSession", MagicMock())
    mocker.patch("app.utils.CSVHandler", MagicMock())
    mocker.patch(
        "app.utils.fetch_and_parse_project_data_to_csv", mock_fetch_and_parse
    )

    await fetch_data_and_save_in_parallel(mock_urls, max_concurrent_tasks)
    assert not max_concurrent_reached


@pytest.mark.asyncio
async def test_fetch_and_parse_project_data_to_csv_valid_url(mocker):
    url = "http://valid-url.com"
    semaphore = asyncio.Semaphore(1)
    session_mock = mocker.MagicMock()
    csv_handler_mock = mocker.MagicMock()

    mocker.patch("app.utils.is_valid_url", return_value=True)
    mocker.patch.object(
        AsyncHTMLDataFetcher, "fetch_data", return_value=mock_html_content
    )
    mocker.patch.object(
        HTMLParsingStrategy,
        "parse",
        return_value=MagicMock(extracted_param="123"),
    )
    mocker.patch.object(
        AsyncJSONDataFetcher, "fetch_data", return_value=mock_json_content
    )
    mocker.patch.object(
        JSONParsingStrategy,
        "parse",
        return_value=ParsedData(
            project_info=ProjectInfo(
                hash="mock", name="mock", floor_count=1, room_count=1
            )
        ),
    )
    mocker.patch.object(CSVHandler, "write_dict_to_csv")

    await fetch_and_parse_project_data_to_csv(
        semaphore, url, session_mock, csv_handler_mock
    )

    AsyncHTMLDataFetcher.fetch_data.assert_called_once_with(url, session_mock)
    HTMLParsingStrategy.parse.assert_called_once()
    AsyncJSONDataFetcher.fetch_data.assert_called_once()
    JSONParsingStrategy.parse.assert_called_once()
    csv_handler_mock.write_dict_to_csv.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_and_parse_project_data_to_csv_invalid_url(mocker):
    url = "http://invalid-url.com"
    semaphore = asyncio.Semaphore(1)
    session_mock = mocker.MagicMock()
    csv_handler_mock = mocker.MagicMock()

    mocker.patch("app.utils.is_valid_url", return_value=False)

    html_fetcher_mock = mocker.patch(
        "app.utils.AsyncHTMLDataFetcher", autospec=True
    )
    html_parser_mock = mocker.patch(
        "app.utils.HTMLParsingStrategy", autospec=True
    )
    json_fetcher_mock = mocker.patch(
        "app.utils.AsyncJSONDataFetcher", autospec=True
    )
    json_parser_mock = mocker.patch(
        "app.utils.JSONParsingStrategy", autospec=True
    )

    await fetch_and_parse_project_data_to_csv(
        semaphore, url, session_mock, csv_handler_mock
    )

    html_fetcher_mock.fetch_data.assert_not_called()
    html_parser_mock.parse.assert_not_called()
    json_fetcher_mock.fetch_data.assert_not_called()
    json_parser_mock.parse.assert_not_called()
    csv_handler_mock.write_dict_to_csv.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_and_parse_project_data_to_csv_parsing_error(mocker):
    url = "http://valid-url-with-parsing-error.com"
    semaphore = asyncio.Semaphore(1)
    session_mock = mocker.MagicMock()
    csv_handler_mock = mocker.MagicMock()

    mocker.patch("app.utils.is_valid_url", return_value=True)
    mocker.patch.object(
        AsyncHTMLDataFetcher, "fetch_data", return_value=mock_html_content
    )
    mocker.patch.object(
        HTMLParsingStrategy,
        "parse",
        return_value=MagicMock(extracted_param=None),
    )  # Simulating parsing error
    mocker.patch.object(
        AsyncJSONDataFetcher, "fetch_data", return_value=mock_json_content
    )
    mocker.patch.object(
        JSONParsingStrategy,
        "parse",
        return_value=MagicMock(project_info=MagicMock()),
    )

    await fetch_and_parse_project_data_to_csv(
        semaphore, url, session_mock, csv_handler_mock
    )

    AsyncHTMLDataFetcher.fetch_data.assert_called_once_with(url, session_mock)
    HTMLParsingStrategy.parse.assert_called_once()
    AsyncJSONDataFetcher.fetch_data.assert_not_called()
    JSONParsingStrategy.parse.assert_not_called()
    csv_handler_mock.write_dict_to_csv.assert_not_called()
