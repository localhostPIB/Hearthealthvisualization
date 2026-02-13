import random
import unittest
from datetime import timedelta, datetime

from faker import Faker

from dao import save_user
from main import init_database
from model import User, GenderEnum
from faker.providers.person.en import Provider
from service import save_heart_service, save_bmi_service


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = init_database()
        self.db = init_database()
        self.fake = Faker("de_DE")
        self.fake.seed_instance(42)

    def _random_datetime(self,startdate, enddate):
        delta = enddate - startdate  # Calculate time span
        random_seconds = random.randint(0, int(delta.total_seconds()))  # Select random seconds
        return startdate + timedelta(seconds=random_seconds)

    def test_1_save_db(self):
        """Saves many heart service records with random dates"""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 12, 31)
        """
        Test-cases.
        """
        user = User(first_name=self.fake.first_name(), last_name=self.fake.last_name() ,age=30, gender=GenderEnum.MALE)
        save_user(user)

        save_heart_service(user_id=user.id,systolic_bp=130, diastolic_bp=90, puls_frequency=85, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=121, diastolic_bp=77, puls_frequency=60, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=78, puls_frequency=65, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=160, diastolic_bp=74, puls_frequency=68, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=81, puls_frequency=57, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=130, diastolic_bp=77, puls_frequency=60, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=111, diastolic_bp=71, puls_frequency=57, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=114, diastolic_bp=70, puls_frequency=54, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=120, diastolic_bp=81, puls_frequency=57, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=71, puls_frequency=53, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=77, puls_frequency=62, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=121, diastolic_bp=77, puls_frequency=67, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=83, puls_frequency=62, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=133, diastolic_bp=81, puls_frequency=56, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=68, puls_frequency=57, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=121, diastolic_bp=69, puls_frequency=61, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=128, diastolic_bp=77, puls_frequency=63, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=114, diastolic_bp=74, puls_frequency=56, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=118, diastolic_bp=77, puls_frequency=63, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=74, puls_frequency=63, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=113, diastolic_bp=74, puls_frequency=61, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=122, diastolic_bp=77, puls_frequency=60, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=74, puls_frequency=59, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=65, puls_frequency=59, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=77, puls_frequency=61, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=78, puls_frequency=56, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=122, diastolic_bp=78, puls_frequency=65, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=65, puls_frequency=59, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=77, puls_frequency=63, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=79, puls_frequency=65, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=119, diastolic_bp=70, puls_frequency=61, date=self._random_datetime(start_date, end_date))
        save_heart_service(user_id=user.id,systolic_bp=111, diastolic_bp=67, puls_frequency=58, date=self._random_datetime(start_date, end_date))

        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=74, puls_frequency=55)
        save_heart_service(user_id=user.id,systolic_bp=117, diastolic_bp=70, puls_frequency=56)
        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=69, puls_frequency=62)
        save_heart_service(user_id=user.id,systolic_bp=123, diastolic_bp=77, puls_frequency=59)

        save_bmi_service(user_id=user.id,weight=112.0, size=1.88, created_at=self._random_datetime(start_date, end_date))


if __name__ == '__main__':
    unittest.main()
