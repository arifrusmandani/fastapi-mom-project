from datetime import datetime
from typing import List
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder

from fastapi import Body, Response
from app.server.database import BaseCRUD
from app.server.models.meeting import MeetingModel, UpdateMeetingModel

from app.server.core.response import ErrorResponseModel, ResponseModel


router = InferringRouter()


@cbv(router)
class MeetingViews:
    model = "meeting_collection"

    @router.post("/", response_description="Berhasil")
    async def add_meeting(self, meeting: MeetingModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        meeting = jsonable_encoder(meeting)
        meeting["created_date"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        new_meeting = await crud.add_data(meeting)
        return ResponseModel(new_meeting, "Meeting added successfully.")

    @router.get("/", response_description="meetings retrieved", response_model=List[MeetingModel])
    async def get_meetings(self):
        crud = BaseCRUD(model=self.model)
        meetings = await crud.get_all()
        return meetings
    
    @router.get("/{id}", response_description="Meeting data retrieved")
    async def get_meeting_detail(self, id):
        crud = BaseCRUD(model=self.model)
        meeting = await crud.get_single(id)
        if meeting:
            return ResponseModel(meeting, "Meeting data retrieved successfully")
        return ErrorResponseModel("An error occurred.", 404, "Meeting doesn't exist.")
    
    @router.put("/{id}")
    async def update_meeting(self, id: str, req: UpdateMeetingModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        meeting = {k: v for k, v in req.dict().items() if v is not None}
        updated_data = await crud.update_data(id, meeting)
        if updated_data:
            return ResponseModel(
                meeting,
                "Meeting updated successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the meeting data.",
        )
    
    @router.delete("/{id}", response_description="Data deleted from the database")
    async def delete_meeting(self, id: str):
        crud = BaseCRUD(model=self.model)
        deleted_data = await crud.delete(id)
        if deleted_data:
            return ResponseModel(
                "Data with ID: {} removed".format(id), "Data deleted successfully"
            )
        return ErrorResponseModel(
            "An error occurred", 404, "Data with id {0} doesn't exist".format(id)
        )