import os
from typing import Final

from dotenv import load_dotenv

from exception import HeathValueNotSaveException, BMIValueNotSaveException, UserNotSaveException, \
    HeartValueNotDeleteException
from model import Heart, BMI, User
from database import Database

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
db = Database(SQLALCHEMY_DATABASE_URL)


def delete_heart_value_by_id(heart_id: int):
    """
    Deletes heart value by id,

    :param heart_id: the id of the heart value.
    """
    try:
        with db.session() as session:
            session.query(Heart).filter_by(id=heart_id).delete()
            session.commit()
    except HeartValueNotDeleteException as e:
        print(e)
        raise e
    finally:
        session.close()

def get_all_users() -> list[User]:
    """
    Outputs a list of all users.

    :returns: User-List
    :rtype: list[User]
    """
    try:
        with db.session() as session:
            return session.query(User).all()
    except UserNotSaveException as e:
        print(e)
        raise e
    finally:
        session.close()

def get_newest_bmi() -> list[BMI]:
    """
    Outputs the first entry from the BMI table.

    :returns: BMI-List.
    :rtype: list[BMI]
    """
    try:
        with db.session() as session:
            return session.query(BMI).order_by(BMI.created_at.desc()).first()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def save_bmi(bmi: BMI):
    """
    Stores the acute BMI value.

    :param bmi: BMI-Object with heart value.
    """
    try:
        with db.session() as session:
            session.add(bmi)
            session.commit()
    except BMIValueNotSaveException as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()


def delete_bmi(bmi_id: int):
    """
    Deletes the BMI entry in the database using the id in the database

    :param bmi_id: the id of the BMI entry.
    """
    try:
        with db.session() as session:
            session.query(Heart).filter_by(id=bmi_id).delete()
            session.commit()
    except BMIValueNotSaveException as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()


def save_heart(heart: Heart):
    """
    Stores the acute heart value.
        
    :param heart: Heart-Object with heart value. 
    """
    try:
        with db.session() as session:
            session.add(heart)
            session.commit()
    except HeathValueNotSaveException as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()


def find_heart_by_id(hid: int) -> Heart:
    """
    Find a heart-object by id.
        
    :param hid: Heart-Object id. 
    :returns: Heart-Object.
    :rtype: Heart
    """
    try:
        with db.session() as session:
            return session.query(Heart).get(hid)
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_all_heart() -> list[Heart]:
    """
    Outputs all heart-objects in a list.

    :returns: List with all heart-objects.
    :rtype: list[Heart]
    """
    try:
        with db.session() as session:
            return session.query(Heart).all()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_all_bmi() -> list[Heart]:
    """
    Outputs all bmi-objects in a list.

    :returns: List with all bmi-objects.
    :rtype: list[Heart]
    """
    try:
        with db.session() as session:
            return session.query(BMI).all()
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()

def save_user(user: User) -> int:
    """
    Stores the User and returns the generated ID.

    :param user: User-Object.
    :return: ID of the saved user.
    """
    try:
        with db.session() as session:
            session.add(user)
            session.commit()

            return user.id
    except BMIValueNotSaveException as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()
