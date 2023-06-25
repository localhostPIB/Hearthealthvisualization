import pandas as pd
from model import Heart
from database import Database

SQLALCHEMY_DATABASE_URL = "sqlite:///hearth_health.sqlite3"
db = Database(SQLALCHEMY_DATABASE_URL)


def save_heart(heart: Heart):
    with db.session() as session:
        session.add(heart)
        session.commit()
        session.close()

def find_heart_by_id(id: int):
    with db.session() as session:
        heart: Heart =  session.query(Heart).get(id)
        session.close()
        return heart

def get_all_heart() -> list[Heart]:
    with db.session() as session:
        list: list[Heart] = session.query(Heart).all()
        session.close()
        return list

