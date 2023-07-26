import json
from typing import Generic, TypeVar
import motor.motor_asyncio
from bson.objectid import ObjectId
from pydantic import BaseModel

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.local


class BaseCRUD():
    def __init__(self, model: str):
        self.model = model
        self.collection = database.get_collection(model)
    
    async def add_data(self, data: dict):
        data = await self.collection.insert_one(data)
        new_data = await self.collection.find_one({"_id": data.inserted_id})
        return new_data
    
    async def get_all(self):
        data = []
        async for student in self.collection.find():
            data.append(student)
        return data
    
    async def get_single(self, id: str):
        data = await self.collection.find_one({"_id": id})
        if data:
            return data
        
    async def get_by_email(self, email: str):
        data = await self.collection.find_one({"email": email})
        if data:
            return data
        
    # Update a student with a matching ID
    async def update_data(self, id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        student = await self.collection.find_one({"_id": id})
        if student:
            updated_student = await self.collection.update_one(
                {"_id": id}, {"$set": data}
            )
            if updated_student:
                return True
            return False
    
    # Delete a student from the database
    async def delete(self, id: str):
        data = await self.collection.find_one({"_id": id})
        if data:
            await self.collection.delete_one({"_id": id})
            return True

student_collection = database.get_collection("students_collection")

def student_helper(student):
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }

# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student into to the database
async def add_student(student_data: dict):
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True