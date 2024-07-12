from sqlalchemy import Column, String, Text

from .base import BaseModel
from .constants import MAXIMUM_NAME_LENGTH


class CharityProject(BaseModel):
    __tablename__ = 'charityproject'
    name = Column(String(MAXIMUM_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
