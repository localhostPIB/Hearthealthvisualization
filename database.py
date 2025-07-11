from contextlib import contextmanager
from typing import Any, Generator
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self, tables) -> None:
        Base.metadata.create_all(self._engine, tables=tables)

    @contextmanager
    def session(self) -> Generator[Session, Any, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            logger.exception("Session rollback because of exception", e)
            session.rollback()
            raise
        finally:
            session.close()
