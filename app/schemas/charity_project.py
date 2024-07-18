from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import (
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    MIN_DESCRIPTION_LENGTH,
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_DESCRIPTION_LENGTH,
    )
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    )
    description: str = Field(
        ...,
        min_length=MIN_DESCRIPTION_LENGTH,
    )
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
