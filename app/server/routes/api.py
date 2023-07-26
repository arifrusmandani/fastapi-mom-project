from fastapi import APIRouter
from app.server.routes.student import api as student
from app.server.routes.meeting import api as meeting
from app.server.routes.user import api as user
from app.server.routes.category import api as category


router = APIRouter()

# router.include_router(student.router, tags=["Student"], prefix="/student")
router.include_router(user.router, tags=["User"], prefix="/user")
router.include_router(meeting.router, tags=["Meeting"], prefix="/meeting")
router.include_router(category.router, tags=["Category"], prefix="/category")