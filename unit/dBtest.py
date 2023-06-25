import unittest

from dao.dao import find_heart_by_id
from service.service import save_heart_service
from main import init_database
from service import save_heart_service


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
       self.db = init_database()


    def test_1_save_db(self):
        save_heart_service(systolic_BP=10,diastolic_BP=10,puls_Frequency=10)

    def test_2_find_db(self):
        heart = find_heart_by_id(1)

        self.assertNotEquals(heart, None)

if __name__ == '__main__':
    unittest.main()
