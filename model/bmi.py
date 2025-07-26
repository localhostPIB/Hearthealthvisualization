from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from database import Base


class BMI(Base):
    """
    BMI values Model for OR-Mapper.
    """
    __tablename__ = 'bmi'

    id: Mapped[int] = Column(Integer, primary_key=True)
    weight: Mapped[Float] = Column(Float)
    size: Mapped[Float] = Column(Float)
    created_at : Mapped[DateTime] = Column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="bmi_value")
    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=False)

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
