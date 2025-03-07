import os

from dotenv import load_dotenv

from exception import HeathValueNotSaveException
from model import Heart
from database import Database


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
db = Database(SQLALCHEMY_DATABASE_URL)


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
        raise e
    finally:
        session.rollback()
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
            heart: Heart = session.query(Heart).get(hid)

            return heart
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_all_heart() -> list[Heart]:
    """
    Outputs all heart-objects in a list.

    :returns: List with all heart-objects.
    :rtype: list
    """
    try:
        with db.session() as session:
            list: list[Heart] = session.query(Heart).all()

            return list
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
