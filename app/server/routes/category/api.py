from datetime import datetime
from typing import List
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder

from fastapi import Body, Response
from app.server.database import BaseCRUD
from app.server.models.category import CategoryModel, UpdateCategoryModel

from app.server.core.response import ErrorResponseModel, ResponseModel


router = InferringRouter()


@cbv(router)
class CategoryViews:
    model = "category_collection"

    @router.post("/", response_description="Berhasil")
    async def add_category(self, category: CategoryModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        category = jsonable_encoder(category)
        category["created_date"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        new_category = await crud.add_data(category)
        return ResponseModel(new_category, "category added successfully.")

    @router.get("/", response_description="categorys retrieved", response_model=List[CategoryModel])
    async def get_categorys(self):
        crud = BaseCRUD(model=self.model)
        datas = await crud.get_all()
        return datas
    
    @router.get("/{id}", response_description="category data retrieved")
    async def get_category_detail(self, id):
        crud = BaseCRUD(model=self.model)
        category = await crud.get_single(id)
        if category:
            return ResponseModel(category, "category data retrieved successfully")
        return ErrorResponseModel("An error occurred.", 404, "category doesn't exist.")
    
    @router.put("/{id}")
    async def update_category(self, id: str, req: UpdateCategoryModel = Body(...)):
        crud = BaseCRUD(model=self.model)
        category = {k: v for k, v in req.dict().items() if v is not None}
        updated_data = await crud.update_data(id, category)
        if updated_data:
            return ResponseModel(
                category,
                "category updated successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the category data.",
        )
    
    @router.delete("/{id}", response_description="Data deleted from the database")
    async def delete_category(self, id: str):
        crud = BaseCRUD(model=self.model)
        deleted_data = await crud.delete(id)
        if deleted_data:
            return ResponseModel(
                "Data with ID: {} removed".format(id), "Data deleted successfully"
            )
        return ErrorResponseModel(
            "An error occurred", 404, "Data with id {0} doesn't exist".format(id)
        )