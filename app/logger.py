import logging
import sys

from app.config import LOGGER_FORMAT

# Define logger
logger = logging.getLogger("p5d_gallery")
logger.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(LOGGER_FORMAT)

# Create stream handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(stream_handler)
