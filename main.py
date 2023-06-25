from tkinter import Tk

from database import Database
from model import Heart
from gui import MainFrame


def init_database():
    SQLALCHEMY_DATABASE_URL = "sqlite:///hearth_health.sqlite3"
    db = Database(SQLALCHEMY_DATABASE_URL)

    db.create_database(tables=[Heart.__table__])

    return db


if __name__ == '__main__':
    root = Tk()
    root.minsize(1050, 400)
    root.maxsize(1050, 400)
    init_database()
    mf = MainFrame(root)
    root.mainloop()
