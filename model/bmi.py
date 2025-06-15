from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime

from database import Base


class BMI(Base):
    """
    BMI values Model for OR-Mapper.
    """
    __tablename__ = 'bmi'

    id = Column(Integer, primary_key=True)
    weight = Column(Float)
    size = Column(Float)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def calc_bmi(self) -> float:
        """
        Calculates the current Body-Mass-Index (BMI).

        :returns: the BMI of the User.
        :rtype: float
        """
        return self.weight / (self.size ** 2)

    def __repr__(self):
        return "%s %s %s" % (
            self.weight,
            self.size,
            self.date
        )
