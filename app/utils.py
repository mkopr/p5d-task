import asyncio
from dataclasses import asdict
from typing import List
from urllib.parse import urlparse

import aiohttp

from app.config import CSV_FILE_PATH, PLANNER5D_API_PROJECT_URL
from app.csv_handler import CSVHandler
from app.fetchers import AsyncHTMLDataFetcher, AsyncJSONDataFetcher
from app.logger import logger
from app.parsers import HTMLParsingStrategy, JSONParsingStrategy


async def fetch_and_parse_project_data_to_csv(
    semaphore: asyncio.Semaphore,
    url: str,
    session: aiohttp.ClientSession,
    csv_handler: CSVHandler,
) -> None:
    """
    Asynchronously fetches and parses data for a given URL, handling errors gracefully.

    :param semaphore: Semaphore to limit the number of concurrent fetches.
    :param url: The URL to fetch data from.
    :param session: The aiohttp ClientSession to use for fetching data.
    :param csv_handler: The CSVHandler instance to use for writing to CSV file.
    """
    async with semaphore:
        # Validate URL
        if not is_valid_url(url):
            logger.error(f"Invalid URL provided: {url}")
            return

        # Fetch HTML data asynchronously
        html_data = await AsyncHTMLDataFetcher().fetch_data(url, session)

        # Parse HTML data synchronously
        html_result = HTMLParsingStrategy().parse(html_data)

        if not html_result.extracted_param:
            logger.error(f"Could not form API URL from HTML data for: {url}")
            return

        # Form the API URL based on parsed HTML data
        url_api = f"{PLANNER5D_API_PROJECT_URL}{html_result.extracted_param}/"

        # Fetch JSON data asynchronously
        json_data = await AsyncJSONDataFetcher().fetch_data(url_api, session)

        # Parse JSON data synchronously
        json_result = JSONParsingStrategy().parse(json_data)

        # Write to CSV file
        csv_handler.write_dict_to_csv(asdict(json_result.project_info))


def form_api_url(project_id: str) -> str:
    """
    Forms the API URL for a given project ID.

    :param project_id: The project ID to form the URL for.
    :return: The API URL for the given project ID.
    """
    return f"{PLANNER5D_API_PROJECT_URL}{project_id}/"


async def fetch_data_and_save_in_parallel(
    urls: List[str], max_concurrent_tasks: int
) -> None:
    """
    Asynchronously fetches data for each unique URL in parallel, with a limit on the number of concurrent tasks.
    Creates an instance of CSVHandler to write to CSV file and closes it after all tasks are completed.

    :param urls: The list of URLs to fetch data from.
    :param max_concurrent_tasks: The maximum number of concurrent tasks to run.
    """
    csv_handler = CSVHandler(CSV_FILE_PATH)
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(max_concurrent_tasks)
        tasks = [
            fetch_and_parse_project_data_to_csv(sem, url, session, csv_handler)
            for url in urls
        ]
        csv_handler.close()
        await asyncio.gather(*tasks)


def is_valid_url(url: str) -> bool:
    """
    Validates the given URL.

    :param url: The URL to be validated.
    :return: True if the URL is valid, False otherwise.
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)
