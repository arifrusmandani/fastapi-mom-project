from datetime import datetime, timedelta
from typing import List
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder

from fastapi import Body, HTTPException, Response, status
from app.server.core.hashing import Hasher
from app.server.database import BaseCRUD
from app.server.models.user import LoginSchema, UserModel, UpdateUserModel, CreateUserModel

from app.server.core.response import ErrorResponseModel, ResponseModel
from app.server.routes.user.object import authenticate_user


router = InferringRouter()


@cbv(router)
class UserViews:
    model = "user_collection"

    @router.post("/", response_description="Berhasil")
    async def add_user(self, user: CreateUserModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        user = jsonable_encoder(user)
        hashed_pwd = Hasher.get_password_hash(user.get("password"))
        user["password"] = hashed_pwd
        user["created_date"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        new_user = await crud.add_data(user)
        return ResponseModel(new_user, "user added successfully.")

    @router.get("/", response_description="users retrieved", response_model=List[UserModel])
    async def get_users(self):
        crud = BaseCRUD(model=self.model)
        users = await crud.get_all()
        return users
    
    @router.get("/{id}", response_description="user data retrieved", response_model=UserModel)
    async def get_user_detail(self, id):
        crud = BaseCRUD(model=self.model)
        user = await crud.get_single(id)
        return user
    
    @router.put("/{id}")
    async def update_user(self, id: str, req: UpdateUserModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        user = {k: v for k, v in req.dict().items() if v is not None}
        updated_data = await crud.update_data(id, user)
        if updated_data:
            return ResponseModel(
                user,
                "user updated successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the user data.",
        )
    
    @router.delete("/{id}", response_description="Data deleted from the database")
    async def delete_user(self, id: str):
        crud = BaseCRUD(model=self.model)
        deleted_data = await crud.delete(id)
        if deleted_data:
            return ResponseModel(
                "Data with ID: {} removed".format(id), "Data deleted successfully"
            )
        return ErrorResponseModel(
            "An error occurred", 404, "Data with id {0} doesn't exist".format(id)
        )

    @router.post("/auth")
    async def auth_login(self, request: LoginSchema):
        user = await authenticate_user(email=request.email, password=request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        return user