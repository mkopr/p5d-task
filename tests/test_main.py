from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from lxml import html

from app.main import app
from tests.mock_data_helpers import get_mock_data_file_path, read_mock_data

# Preparing mock data
mock_html_content = read_mock_data("html", "dummy_page.html")
mock_json_content = read_mock_data("json", "dummy_api.json")
mock_csv_content = read_mock_data("csv", "dummy_file.csv")
mock_csv_path = get_mock_data_file_path("csv", "dummy_file.csv")


@pytest.mark.asyncio
async def test_main_page():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    parsed_html = html.fromstring(response.content)

    generate_csv_button = parsed_html.xpath("//button[text()='Generate CSV']")
    assert len(generate_csv_button) == 1
    assert "display:none" not in generate_csv_button[0].get("style", "")

    download_csv_button = parsed_html.xpath("//button[@id='downloadButton']")
    assert len(download_csv_button) == 1
    assert "display:none" in download_csv_button[0].get("style", "")


@pytest.mark.asyncio
async def test_generate_csv(mocker):
    mocker.patch(
        "app.fetchers.AsyncHTMLDataFetcher.fetch_data",
        new_callable=AsyncMock,
        return_value=mock_html_content,
    )
    mocker.patch(
        "app.fetchers.AsyncJSONDataFetcher.fetch_data",
        new_callable=AsyncMock,
        return_value=mock_json_content,
    )
    mocker.patch(
        "app.csv_handler.CSVHandler.write_dict_to_csv",
        new_callable=MagicMock,
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/generate-csv")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_download_csv():
    with patch("app.main.CSV_FILE_PATH", new=mock_csv_path):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/download-csv")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

    with open(mock_csv_path, "r") as file:
        content = file.read()

    assert content == mock_csv_content
