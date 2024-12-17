import os

from nicegui import ui
from dotenv import load_dotenv
from database import Database
from gui import build_gui
from model import Heart

load_dotenv()

def init_database():
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
    db = Database(SQLALCHEMY_DATABASE_URL)

    db.create_database(tables=[Heart.__table__])

    return db


if __name__ in {"__main__", "__mp_main__"}:
    init_database()
    build_gui()
    ui.run(native=True, favicon='🫀', frameless=True, fullscreen=True, language="de")
