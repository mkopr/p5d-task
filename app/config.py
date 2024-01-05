import os
from typing import Final, List

# Maximum number of concurrent tasks
MAX_CONCURRENT_TASKS: Final[int] = 3

# List of 25 URLs from https://planner5d.com/gallery/floorplans/
LIST_OF_PROJECTS: Final[List[str]] = [
    "https://planner5d.com/gallery/floorplans/LTXdJG/floorplans-house-terrace-decor-diy-landscape-3d",
    "https://planner5d.com/gallery/floorplans/LJePOG/floorplans-house-3d",
    "https://planner5d.com/gallery/floorplans/LJcePG/floorplans-house-terrace-furniture-decor-bedroom-3d",
    "https://planner5d.com/gallery/floorplans/LJZPOG/floorplans-house-decor-lighting-dining-room-3d",
    "https://planner5d.com/gallery/floorplans/LJSSLG/floorplans-bedroom-3d",
    "https://planner5d.com/gallery/floorplans/LJXXfG/floorplans-house-decor-outdoor-lighting-architecture-3d",
    "https://planner5d.com/gallery/floorplans/LJfTfG/floorplans-apartment-kitchen-renovation-architecture-3d",
    "https://planner5d.com/gallery/floorplans/LJfTGG/floorplans-architecture-3d",
    "https://planner5d.com/gallery/floorplans/LJfTSG/floorplans-living-room-3d",
    "https://planner5d.com/gallery/floorplans/LJfTOG/floorplans-house-3d",
    "https://planner5d.com/gallery/floorplans/LJfHSG/floorplans-house-decor-living-room-lighting-3d",
    "https://planner5d.com/gallery/floorplans/LJfGLG/floorplans-kitchen-3d",
    "https://planner5d.com/gallery/floorplans/LJdccG/floorplans-apartment-furniture-bedroom-living-room-kitchen-3d",
    "https://planner5d.com/gallery/floorplans/LPJaZZ/floorplans-house-terrace-furniture-decor-3d",
    "https://planner5d.com/gallery/floorplans/LXHZXG/floorplans-house-furniture-decor-outdoor-3d",
    "https://planner5d.com/gallery/floorplans/LTfGcG/floorplans-house-architecture-3d",
    "https://planner5d.com/gallery/floorplans/LXSdaG/floorplans-house-furniture-decor-lighting-household-3d",
    "https://planner5d.com/gallery/floorplans/LGHGaZ/floorplans-house-diy-architecture-3d",
    "https://planner5d.com/gallery/floorplans/LHadbZ/floorplans-house-terrace-outdoor-architecture-3d",
    "https://planner5d.com/gallery/floorplans/ePJfa/floorplans-apartment-3d",
    "https://planner5d.com/gallery/floorplans/ccGGe/floorplans-kitchen-3d",
    "https://planner5d.com/gallery/floorplans/JeGae/floorplans-3d",
    "https://planner5d.com/gallery/floorplans/JJHbZ/floorplans-3d",
    "https://planner5d.com/gallery/floorplans/JPJfG/floorplans-3d",
    "https://planner5d.com/gallery/floorplans/JGSGZ/floorplans-3d",
]

# CSV file setup
CSV_FILE_NAME: Final[str] = "download-csv.csv"
CSV_FILE_FOLDER: Final[str] = "files"
CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__), CSV_FILE_FOLDER, CSV_FILE_NAME
)

# url to API with planner 5d projects
PLANNER5D_API_PROJECT_URL: Final[str] = "https://planner5d.com/api/project/"

# xpath to get project id from floorplans page html
PROJECT_ID_XPATH: Final[
    str
] = "/html/body/main/div/div/aside/div[2]/div[1]/a/@href"
MAIN_PAGE_HTML_PATH: Final[str] = "app/static/index.html"

# logger format
LOGGER_FORMAT: Final[
    str
] = "[%(levelname)s][%(asctime)s][%(filename)s][%(funcName)s][%(lineno)d] %(message)s"
