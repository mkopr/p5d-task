from unittest.mock import MagicMock

import aiohttp
import pytest

from app.fetchers import AsyncHTMLDataFetcher, AsyncJSONDataFetcher
from tests.mock_data_helpers import mock_get, read_mock_data


class TestAsyncHTMLDataFetcher:
    @pytest.mark.asyncio
    async def test_fetch_data_success(self):
        test_url = "http://example.com"
        mock_html_content = read_mock_data("html", "dummy_page.html")

        mock_session = MagicMock()
        mock_session.get.side_effect = mock_get(mock_html_content)

        fetcher = AsyncHTMLDataFetcher()

        result = await fetcher.fetch_data(test_url, mock_session)

        assert result == mock_html_content

    @pytest.mark.asyncio
    async def test_fetch_data_failure(self):
        test_url = "invalid-url"

        mock_session = MagicMock()
        mock_session.get.side_effect = aiohttp.InvalidURL(test_url)

        fetcher = AsyncHTMLDataFetcher()

        result = await fetcher.fetch_data(test_url, mock_session)

        mock_session.get.assert_called_once_with(test_url)
        assert result is None


class TestAsyncJSONDataFetcher:
    @pytest.mark.asyncio
    async def test_fetch_json_data_success(self):
        test_url = "http://example.com/api/data"
        mock_json_content = read_mock_data("json", "dummy_api.json")

        mock_session = MagicMock()
        mock_session.get.side_effect = mock_get(mock_json_content)

        fetcher = AsyncJSONDataFetcher()

        result = await fetcher.fetch_data(test_url, mock_session)

        assert result == mock_json_content

    @pytest.mark.asyncio
    async def test_fetch_json_data_failure(self):
        test_url = "invalid-url"

        mock_session = MagicMock()
        mock_session.get.side_effect = aiohttp.InvalidURL(test_url)

        fetcher = AsyncJSONDataFetcher()

        result = await fetcher.fetch_data(test_url, mock_session)

        mock_session.get.assert_called_once_with(test_url)
        assert result is None
