from fastapi import APIRouter

from app.api.api_v1.endpoints import todos, address, users, auth

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(todos.router)
api_router.include_router(address.router)
