from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseModel


class Donation(BaseModel):
    __tablename__ = 'donation'
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
