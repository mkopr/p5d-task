from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

from app.config import (
    CSV_FILE_PATH,
    LIST_OF_PROJECTS,
    MAIN_PAGE_HTML_PATH,
    MAX_CONCURRENT_TASKS,
)
from app.logger import logger
from app.utils import fetch_data_and_save_in_parallel

app = FastAPI()


@app.get("/")
async def main_page():
    """
    Serves the main page.
    """
    logger.info("Serving main page")
    return FileResponse(MAIN_PAGE_HTML_PATH)


@app.get("/generate-csv")
async def generate_csv():
    """
    Fetches data from a list of URLs and saves it to a CSV file.
    """
    await fetch_data_and_save_in_parallel(
        LIST_OF_PROJECTS, MAX_CONCURRENT_TASKS
    )
    return Response(status_code=200)


@app.get("/download-csv", response_class=FileResponse)
async def download_csv():
    """
    Downloads the CSV file.
    """
    return FileResponse(CSV_FILE_PATH)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run(app)
