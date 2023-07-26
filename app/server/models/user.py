from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from app.server.models import PyObjectId

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    phone: str
    date_of_birth: str
    gender: str
    role: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@x.edu.ng",
                "password": "Password.1",
                "phone": "0898090909",
                "date_of_birth": "1998-09-01",
                "gender": "MALE",
                "role": "superadmin"
            }
        }

class CreateUserModel(UserModel):
    password: str

class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    role: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe Update",
                "email": "jdoe2@x.edu.ng",
                "password": "Password.1",
                "phone": "089812392000",
                "date_of_birth": "1998-09-01",
                "gender": "MALE",
                "role": "superadmin",
            }
        }

class LoginSchema(BaseModel):
    email: str
    password: str