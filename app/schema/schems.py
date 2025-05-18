from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime


class PersonBase(BaseModel):
    name: str
    age: int
    marks: int

class PersonUpdateBase(BaseModel):
    name: str | None = None
    age: int | None = None
    marks: int | None = None


# Boys
class BoyBase(PersonBase):
    pass


class BoyCreate(BoyBase):
    pass


class BoyUpdate(PersonUpdateBase):
    pass


class Boy(BoyBase):
    boy_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "boy_id": 1,
                "name": "Alex",
                "age": 15,
                "marks": 85
            }
        }
    )


# Girls
class GirlBase(PersonBase):
    pass


class GirlCreate(GirlBase):
    pass


class GirlUpdate(PersonUpdateBase):
    pass


class Girl(GirlBase):
    girl_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "girl_id": 1,
                "name": "Dasha",
                "age": 18,
                "marks": 66
            }
        }
    )


# PairReviews
class ReviewBase(BaseModel):
    boy_id: int
    girl_id: int
    review: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    review: Optional[str] = None


class Review(ReviewBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "boy_id": 1,
                "girl_id": 1,
                "review": "Lubov silna"
            }
        }
    )

# Conscription
class ConscriptionBase(BaseModel):
    is_fit: bool
    reason: Optional[str] = None


class ConscriptionCreate(ConscriptionBase):
    boy_id: int


class ConscriptionUpdate(ConscriptionBase):
    is_fit: Optional[bool] = None


class Conscription(ConscriptionBase):
    conscription_id: int
    boy_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "conscription_id": 1,
                "boy_id": 1,
                "is_fit": "True",
                "reason": "Lost his brain/jet brain"
            }
        }
    )
