# Planner 5D Gallery CSV Generator

This project automates the extraction of project data from the Planner 5D gallery (https://planner5d.com/gallery/floorplans) and generates a CSV file. 
The primary goal is to select at least 25 projects, extract specific details, and output them directly into a CSV file.

## Prerequisites

- Docker
- Docker Compose  
https://docs.docker.com/compose/install/

## Installation and Setup

1. Clone the git bundle:  
`git clone p5d_gallery.bundle p5d_gallery`
  
2. Install Docker and Docker Compose if not already installed.
3. Navigate to the project directory.

## Running the Application

Use the following `make` commands to manage the application:

quick command to build and start project with log view:  
`make up-b && make logs`

### Available commands:  
- `make build`: Build the project.
- `make up`: Start the project.
- `make up-b`: Build and start the project.
- `make down`: Stop the project.
- `make down-v`: Stop the project and remove containers.
- `make logs`: Show logs.
- `make test`: Run tests.
- `make lint`: Run linting and type check.

Access the application at `http://0.0.0.0:8000/`.

## Using the Application

1. Open the application in browser
2. Click *Generate CSV*.
3. Wait for the download button.
4. Click *Download CSV* and save the CSV file.
5. File stored in `app/files` folder.

## Configuration and Customization
Configuration is done in `app/config.py` file

### Configuration options:
`MAX_CONCURRENT_TASKS`: Control the number of simultaneous requests.  
`LIST_OF_PROJECTS`: Specify URLs for data extraction.  
`CSV_FILE_NAME`, `CSV_FILE_FOLDER`: Define CSV file naming and storage location.  
`PLANNER5D_API_PROJECT_URL`: Set the API URL for Planner 5D projects.  
`PROJECT_ID_XPATH`: XPath for project ID extraction from HTML.  
`MAIN_PAGE_HTML_PATH`: Path to the main HTML file.  

## Linting and Code Formatting

Code formatted with flake8, black.
Typing checked with mypy.

Run the following command for linting & type check: `make lint`

## Testing

Tests and mock files in the `tests` folder.  
Run the following command for testing: `make test`

## Dependencies
- python 3.11 alpine: Base image for the application.   
- fastAPI: Web framework for building APIs.  
- uvicorn: An ASGI server for Python, serving FastAPI applications.  
- aiohttp, httpx: Asynchronous HTTP client/server frameworks.  
- lxml: Library for processing XML and HTML.  
- pytest: Testing framework.  
- flake8: Linting tool.  
- black: Code formatter.  
- mypy: Static type checker.  

## Future Enhancements
1. Integration of URL Management from Text Files
For handling larger datasets, it would be beneficial to implement a feature where the floorplan URLs are read from a text file. 
This approach simplifies the process of updating and managing extensive lists of URLs. 
The text file can be structured with one URL per line, allowing easy additions or removals.

2. Automated Floorplan Collection
To further automate the process, integrating a web scraping tool like Selenium or BeautifulSoup can be very useful. 
Specifically, the project can be enhanced to automatically scrape floorplan URLs from websites like Planner 5D Floorplans. 
This would involve writing a script that navigates the site, extracts the relevant URLs, and saves them, potentially into the aforementioned text file. 
This feature would significantly reduce manual effort and streamline the process of gathering diverse floorplan designs for analysis or other purposes.

## Inconsistency in API Fields Format
While integrating the Planner 5D API, an inconsistency was discovered in the format of one of the API records. 
Specifically, the API endpoint https://planner5d.com/api/project/066bf153da900c999647183638120d65/ returned data `items[0]["data"]` where the field formats were not consistent across different records.