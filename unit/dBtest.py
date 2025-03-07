import unittest
from main import init_database
from service import save_heart_service


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = init_database()

    def test_1_save_db(self):
        """
        Test-cases.
        """
        save_heart_service(systolic_bp=120, diastolic_bp=77, puls_frequency=63)
        save_heart_service(systolic_bp=121, diastolic_bp=77, puls_frequency=60)
        save_heart_service(systolic_bp=119, diastolic_bp=78, puls_frequency=65)
        save_heart_service(systolic_bp=118, diastolic_bp=74, puls_frequency=68)

        save_heart_service(systolic_bp=123, diastolic_bp=81, puls_frequency=57)
        save_heart_service(systolic_bp=130, diastolic_bp=77, puls_frequency=60)
        save_heart_service(systolic_bp=111, diastolic_bp=71, puls_frequency=57)
        save_heart_service(systolic_bp=114, diastolic_bp=70, puls_frequency=54)

        save_heart_service(systolic_bp=120, diastolic_bp=81, puls_frequency=57)
        save_heart_service(systolic_bp=117, diastolic_bp=71, puls_frequency=53)
        save_heart_service(systolic_bp=119, diastolic_bp=77, puls_frequency=62)
        save_heart_service(systolic_bp=121, diastolic_bp=77, puls_frequency=67)

        save_heart_service(systolic_bp=123, diastolic_bp=83, puls_frequency=62)
        save_heart_service(systolic_bp=133, diastolic_bp=81, puls_frequency=56)
        save_heart_service(systolic_bp=123, diastolic_bp=68, puls_frequency=57)
        save_heart_service(systolic_bp=121, diastolic_bp=69, puls_frequency=61)

        save_heart_service(systolic_bp=128, diastolic_bp=77, puls_frequency=63)
        save_heart_service(systolic_bp=114, diastolic_bp=74, puls_frequency=56)
        save_heart_service(systolic_bp=118, diastolic_bp=77, puls_frequency=63)
        save_heart_service(systolic_bp=119, diastolic_bp=74, puls_frequency=63)

        save_heart_service(systolic_bp=113, diastolic_bp=74, puls_frequency=61)
        save_heart_service(systolic_bp=122, diastolic_bp=77, puls_frequency=60)
        save_heart_service(systolic_bp=123, diastolic_bp=74, puls_frequency=59)
        save_heart_service(systolic_bp=117, diastolic_bp=65, puls_frequency=59)

        save_heart_service(systolic_bp=119, diastolic_bp=77, puls_frequency=61)
        save_heart_service(systolic_bp=117, diastolic_bp=78, puls_frequency=56)
        save_heart_service(systolic_bp=122, diastolic_bp=78, puls_frequency=65)
        save_heart_service(systolic_bp=117, diastolic_bp=65, puls_frequency=59)

        save_heart_service(systolic_bp=123, diastolic_bp=77, puls_frequency=63)
        save_heart_service(systolic_bp=119, diastolic_bp=79, puls_frequency=65)
        save_heart_service(systolic_bp=119, diastolic_bp=70, puls_frequency=61)
        save_heart_service(systolic_bp=111, diastolic_bp=67, puls_frequency=58)

        save_heart_service(systolic_bp=117, diastolic_bp=74, puls_frequency=55)
        save_heart_service(systolic_bp=117, diastolic_bp=70, puls_frequency=56)
        save_heart_service(systolic_bp=123, diastolic_bp=69, puls_frequency=62)
        save_heart_service(systolic_bp=123, diastolic_bp=77, puls_frequency=59)


if __name__ == '__main__':
    unittest.main()
