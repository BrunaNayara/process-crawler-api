import unittest
from unittest.mock import MagicMock

from data_manager import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager()

    def test_get_jtr_code(self):
        expected_jtr_code = "1.12"
        mocked_process_number = "1234567-12.1234." + expected_jtr_code + ".1234"
        jtr_code = self.dm.get_jtr_code(mocked_process_number)
        self.assertEqual(expected_jtr_code, jtr_code)

    def test_matching_pattern_is_valid(self):
        mocked_proc_number = "1234567-12.1234.1.12.1234"
        self.assertTrue(self.dm._is_valid_process_number(mocked_proc_number))

    def test_not_matching_pattern_is_invalid(self):
        mocked_proc_number = "12-12.12.12.12.12"
        self.assertFalse(self.dm._is_valid_process_number(mocked_proc_number))

    def test_get_data_invalid_process_number(self):
        mocked_proc_number = "12-12.12.12.12.12"
        self.dm._is_valid_process_number = MagicMock(return_value=False)
        self.dm.instatiate_crawler = MagicMock()

        actual = self.dm.get_process_data(mocked_proc_number)

        self.dm.instatiate_crawler.assert_not_called()


    def test_get_data_valid_process_number(self):
        expected_jtr_code = "1.12"
        mocked_process_number = "1234567-12.1234." + expected_jtr_code + ".1234"
        mocked_tribunal_crawler = MagicMock()
        expected_data = {"all": "data", "you": "can get"}
        self.dm._is_valid_process_number = MagicMock(return_value=True)
        self.dm.instatiate_crawler = MagicMock(return_value=mocked_tribunal_crawler)
        mocked_tribunal_crawler.extract_data_from_all_graus.return_value = expected_data

        actual = self.dm.get_process_data(mocked_process_number)

        self.assertEqual(expected_data, actual)



if __name__ == '__main__':
    unittest.main()
