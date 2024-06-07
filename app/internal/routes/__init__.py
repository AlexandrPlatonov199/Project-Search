"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application.
"""


from fastapi import APIRouter

from app.pkg.models.core.routes import Routes
from app.pkg.models.exceptions import users

__all__ = [
    "__routes__",
    "user_router",
    "auth_router",
    "profile_router",
]

user_router = APIRouter(
    prefix="/v1/user",
    tags=["User"],
    responses={
        **users.UserNotFound.generate_openapi(),
    },
)

auth_router = APIRouter(prefix="/v1/auth", tags=["Auth"])

profile_router = APIRouter(prefix="/v1/profile", tags=["Profile"])

__routes__ = Routes(
    routers=(
        user_router,
        auth_router,
        profile_router,
    ),
)
