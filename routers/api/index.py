from fastapi import APIRouter

from routers.api import auth, users, todos

router = APIRouter(prefix='/api')
router.include_router(auth.router)
router.include_router(todos.router)
router.include_router(users.router)
