from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from app.server.models import PyObjectId
from datetime import datetime

class CategoryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    created_date: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Weekly Meeting"
            }
        }


class UpdateCategoryModel(BaseModel):
    name: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daily Meeting",
            }
        }