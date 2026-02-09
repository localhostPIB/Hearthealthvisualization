from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from database import Base


class Heart(Base):
    """
    Heart values Model for OR-Mapper.
    """
    __tablename__ = 'heart'

    id: Mapped[int] = Column(Integer, primary_key=True)
    systolic_BP: Mapped[int] = Column(Integer)
    diastolic_BP: Mapped[int] = Column(Integer)
    puls_Frequency: Mapped[int] = Column(Integer)
    date: Mapped[DateTime] = Column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="heart_value")
    user_id: Mapped[int]  = Column(Integer, ForeignKey('user.id'), nullable=False)

    def calc_pulse_pressure(self) -> int:
        return self.systolic_BP - self.diastolic_BP

    def __repr__(self):
        return "%s %s %s %s %s %s" % (
            self.id,
            self.systolic_BP,
            self.diastolic_BP,
            self.calc_pulse_pressure(),
            self.puls_Frequency,
            self.date
        )



