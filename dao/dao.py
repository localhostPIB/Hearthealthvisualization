from exception import HeathValueNotSaveException
from model import Heart
from database import Database

SQLALCHEMY_DATABASE_URL = "sqlite:///hearth_health.sqlite3"
db = Database(SQLALCHEMY_DATABASE_URL)


def save_heart(heart: Heart):
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


def find_heart_by_id(id: int):
    try:
        with db.session() as session:
            heart: Heart = session.query(Heart).get(id)

            return heart
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


def get_all_heart() -> list[Heart]:
    try:
        with db.session() as session:
            list: list[Heart] = session.query(Heart).all()

            return list
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
