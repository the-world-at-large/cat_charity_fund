from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Boolean

from app.core.db import Base
from ..constants import DEFAULT_INVESTMENT_AMOUNT


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_INVESTMENT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime(timezone=True),
                         default=lambda: datetime.now())
    close_date = Column(DateTime(timezone=True), nullable=True)
