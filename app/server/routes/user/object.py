from app.server.core.hashing import Hasher
from app.server.database import BaseCRUD

model = "user_collection"

async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if not user:
        return False
    if not Hasher.verify_password(password, user.get("password")):
        return False
    return user

async def get_user(email: str):
    crud = BaseCRUD(model=model)
    user = await crud.get_by_email(email)
    return user