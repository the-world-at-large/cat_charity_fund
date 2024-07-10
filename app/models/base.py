from sqlalchemy import Column, DateTime, Integer, Boolean, func

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    close_date = Column(DateTime(timezone=True), nullable=True)
