import csv
import os

from app.csv_handler import CSVHandler


class TestCSVHandler:
    test_file = "tests/test.csv"

    @classmethod
    def setup_class(cls):
        """
        Create a test CSV file if it doesn't exist.
        """
        if not os.path.exists(cls.test_file):
            with open(cls.test_file, "w"):
                pass

    @classmethod
    def teardown_class(cls):
        """
        Remove the test file after all tests have run.
        """
        os.remove(cls.test_file)

    def test_singleton_instance(self):
        handler1 = CSVHandler(self.test_file)
        handler2 = CSVHandler(self.test_file)
        assert handler1 is handler2

    def test_write_dict_to_csv(self):
        handler = CSVHandler(self.test_file)
        handler.close()
        test_data = {"column1": "value1", "column2": "value2"}
        handler.write_dict_to_csv(test_data)

        with open(self.test_file, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assert row == test_data

    def test_file_state_handling(self):
        handler = CSVHandler(self.test_file)
        assert not handler.is_closed
        handler.close()
        assert handler.is_closed

    def test_handling_empty_data(self):
        handler = CSVHandler(self.test_file)
        handler.write_dict_to_csv({})
