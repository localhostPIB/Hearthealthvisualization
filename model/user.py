from typing import List

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import Mapped, relationship

from database import Base
from model.GenderEnum import GenderEnum


class User(Base):
    """
    User values Model for OR-Mapper.
    """
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    age: Mapped[int] = Column(Integer, nullable=False)
    gender: Mapped[GenderEnum] = Column(Enum(GenderEnum), nullable=False)

    heart_value: Mapped[List["Heart"]] = relationship("Heart", back_populates="user" ,lazy=True)
    bmi_value: Mapped[List["BMI"]] = relationship("BMI", back_populates="user" ,lazy=True)

    def __repr__(self):
        return "%s %s %s %s" % (
            self.name,
            self.age,
            self.gender,
            self.heart_value
        )