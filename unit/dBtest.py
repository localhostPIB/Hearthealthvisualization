import unittest
from main import init_database
from service import save_heart_service


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = init_database()

    def test_1_save_db(self):
        save_heart_service(systolic_BP=120, diastolic_BP=77, puls_Frequency=63)
        save_heart_service(systolic_BP=121, diastolic_BP=77, puls_Frequency=60)
        save_heart_service(systolic_BP=119, diastolic_BP=78, puls_Frequency=65)
        save_heart_service(systolic_BP=118, diastolic_BP=74, puls_Frequency=68)

        save_heart_service(systolic_BP=123, diastolic_BP=81, puls_Frequency=57)
        save_heart_service(systolic_BP=130, diastolic_BP=77, puls_Frequency=60)
        save_heart_service(systolic_BP=111, diastolic_BP=71, puls_Frequency=57)
        save_heart_service(systolic_BP=114, diastolic_BP=70, puls_Frequency=54)

        save_heart_service(systolic_BP=120, diastolic_BP=81, puls_Frequency=57)
        save_heart_service(systolic_BP=117, diastolic_BP=71, puls_Frequency=53)
        save_heart_service(systolic_BP=119, diastolic_BP=77, puls_Frequency=62)
        save_heart_service(systolic_BP=121, diastolic_BP=77, puls_Frequency=67)

        save_heart_service(systolic_BP=123, diastolic_BP=83, puls_Frequency=62)
        save_heart_service(systolic_BP=133, diastolic_BP=81, puls_Frequency=56)
        save_heart_service(systolic_BP=123, diastolic_BP=68, puls_Frequency=57)
        save_heart_service(systolic_BP=121, diastolic_BP=69, puls_Frequency=61)

        save_heart_service(systolic_BP=128, diastolic_BP=77, puls_Frequency=63)
        save_heart_service(systolic_BP=114, diastolic_BP=74, puls_Frequency=56)
        save_heart_service(systolic_BP=118, diastolic_BP=77, puls_Frequency=63)
        save_heart_service(systolic_BP=119, diastolic_BP=74, puls_Frequency=63)

        save_heart_service(systolic_BP=113, diastolic_BP=74, puls_Frequency=61)
        save_heart_service(systolic_BP=122, diastolic_BP=77, puls_Frequency=60)
        save_heart_service(systolic_BP=123, diastolic_BP=74, puls_Frequency=59)
        save_heart_service(systolic_BP=117, diastolic_BP=65, puls_Frequency=59)

        save_heart_service(systolic_BP=119, diastolic_BP=77, puls_Frequency=61)
        save_heart_service(systolic_BP=117, diastolic_BP=78, puls_Frequency=56)
        save_heart_service(systolic_BP=122, diastolic_BP=78, puls_Frequency=65)
        save_heart_service(systolic_BP=117, diastolic_BP=65, puls_Frequency=59)

        save_heart_service(systolic_BP=123, diastolic_BP=77, puls_Frequency=63)
        save_heart_service(systolic_BP=119, diastolic_BP=79, puls_Frequency=65)
        save_heart_service(systolic_BP=119, diastolic_BP=70, puls_Frequency=61)
        save_heart_service(systolic_BP=111, diastolic_BP=67, puls_Frequency=58)

        save_heart_service(systolic_BP=117, diastolic_BP=74, puls_Frequency=55)
        save_heart_service(systolic_BP=117, diastolic_BP=70, puls_Frequency=56)
        save_heart_service(systolic_BP=123, diastolic_BP=69, puls_Frequency=62)
        save_heart_service(systolic_BP=123, diastolic_BP=77, puls_Frequency=59)


if __name__ == '__main__':
    unittest.main()
