import csv
import os
from typing import Dict, Optional

from app.logger import logger


class CSVHandler:
    """
    Singleton class to handle CSV file operations.

    Attributes:
        _instance (CSVHandler): The single instance of the class.
        file_path (str): The path to the CSV file.
        is_closed (bool): Indicates whether the file is closed.
    """

    _instance: Optional["CSVHandler"] = None
    is_closed: bool = False
    file_path = ""

    def __new__(cls, file_path: str) -> "CSVHandler":
        """
        Create a new instance of CSVHandler if one doesn't exist.
        Follows the Singleton design pattern.

        :param file_path: Path to the CSV file.
        :return: Instance of CSVHandler.
        """
        if cls._instance is None:
            cls._instance = super(CSVHandler, cls).__new__(cls)
            cls._instance.file_path = file_path
            cls._instance.is_closed = False
        return cls._instance

    def write_dict_to_csv(self, data: Dict[str, str]) -> None:
        """
        Writes a single dictionary entry to a CSV file.

        :param data: A dictionary to write to the CSV file.
                     The dictionary represents a row, with keys as column headers.
        :return: None
        """
        if not data:
            return  # No data to write

        mode = "w" if self.is_closed else "a"
        file_exists = os.path.isfile(self.file_path) and not self.is_closed

        try:
            with open(self.file_path, mode, newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())

                if not file_exists or self.is_closed:
                    writer.writeheader()  # Write header for new or closed file

                writer.writerow(data)
                self.is_closed = False  # Reset the flag as file is now open

        except IOError as e:
            logger.error(f"IOError: {e}")

    def close(self) -> None:
        """
        Marks the file as closed.
        """
        self.is_closed = True
