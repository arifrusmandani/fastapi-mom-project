from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from pydantic import BaseModel, Field

from app.server.models import PyObjectId

class MeetingSchema(BaseModel):
    title: str
    description: str
    summary: str
    is_public: bool
    members: List = []
    time_and_date: str
    created_date: str
    user_id: str
    category_id: str

    class Config:
        schema_extra = {
            "example": {
                "title": "John Doe",
                "description": "jdoe@x.edu.ng",
                "summary": "Water resources engineering",
                "is_public": True,
                "members": ["Arif"],
                "time_and_date": "2023-01-01 10:10:10",
                "created_date": "2023-01-01",
                "user_id": "11",
                "category_id": "12",
            }
        }
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str  # Convert ObjectId to str
        }


class MeetingModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    summary: str
    is_public: bool
    members: List = []
    shared_to: List = []
    time_and_date: str
    created_date: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    created_by: str
    category_code: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Performance Adjustment API",
                "description": "Performance adjusmnet llllllll",
                "summary": "Water resources engineering",
                "is_public": True,
                "members": ["Arif"],
                "shared_to": [],
                "time_and_date": "2023-01-01 10:10:10",
                "created_by": "Arif",
                "category_code": "Weekly Meeting",
            }
        }


class UpdateMeetingModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    summary: Optional[str]
    is_public: Optional[bool]
    members: List = []
    time_and_date: Optional[str]
    category_code: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "John Doe",
                "description": "jdoe@x.edu.ng",
                "summary": "Water resources engineering",
                "is_public": True,
                "members": ["Arif"],
                "time_and_date": "2023-01-01 10:10:10",
                "category_code": "12",
            }
        }