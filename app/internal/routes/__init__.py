"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application.
"""


from fastapi import APIRouter

from app.pkg.models.core.routes import Routes

__all__ = [
    "__routes__",
    "user_router",
]

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


__routes__ = Routes(
    routers=(
        user_router,
    ),
)
