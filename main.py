import os
import sys

from nicegui import ui, native
from dotenv import load_dotenv

from database import Database
from gui import build_gui
from model import Heart, BMI, User

load_dotenv()


def init_database():
    """Initializes the database and the OR-mapper."""
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
    db = Database(SQLALCHEMY_DATABASE_URL)

    db.create_database(tables=[Heart.__table__, BMI.__table__, User.__table__])

    return db


if __name__ in {"__main__", "__mp_main__"}:
    """
    Starts the actual application (Nicegui) using sys.argv you can set how the application should be started
    
    Arguments sys.argv[1]: Means whether you want to start the application in the browser or in its own window, 
    the latter is often not possible under Ubuntu.
    
    Arguments sys.argv[2]: Specifies a port.
    
    Arguments sys.argv[3]: If the argv is set to automatic then nicegui searches for any free port in the system. 
    Otherwise, enter the port specified by the user (from sys.argv[2]) Port
    """ 
    init_database()
    build_gui()

    if len(sys.argv) != 4:
        ui.run(native=True, favicon='🫀', frameless=True, fullscreen=True, language="de", port=native.find_open_port())
    else:
        is_native = (sys.argv[1].lower() == "native")

        if sys.argv[3] == "automatic":
            port_str = native.find_open_port()
        else:
            port_str = sys.argv[2]

        ui.run(native=is_native, favicon='🫀', frameless=is_native, fullscreen=is_native, language="de", port=int(port_str))
