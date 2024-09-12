from fastapi import APIRouter

from routers.api import users

router = APIRouter(prefix='/api')
router.include_router(users.router)
