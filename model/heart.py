from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from database import Base


class Heart(Base):
    """
    Heart values Model for OR-Mapper.
    """
    __tablename__ = 'heart'

    id = Column(Integer, primary_key=True)
    systolic_BP = Column(Integer)
    diastolic_BP = Column(Integer)
    puls_Frequency = Column(Integer)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "%s %s %s %s" % (
          self.systolic_BP,
          self.diastolic_BP,
          self.puls_Frequency,
          self.date
        )
