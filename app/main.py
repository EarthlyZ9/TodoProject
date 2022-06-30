from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings

description = """
    TODO Project API 🚀

    ## Todos

    You can **CRUD Todos**.

    ## Users

    This includes:

"""

tags_metadata = [
    {
        "name": "Todos",
        "description": "Operations with todo items",
    },
    {
        "name": "Auth",
        "description": "Authentication and authorization",
    },
    {
        "name": "Users",
        "description": "User management",
    },
    {
        "name": "Address",
        "description": "Address information for users",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="0.0.1",
    contact={
        "name": "Earthly Jisoo",
        "url": "https://github.com/linda2927",
        "email": "earthlyz9.dev@gmail.com",
    },
    openapi_tags=tags_metadata,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
