import uuid

from pydantic import BaseModel


__all__ = ["JWTData",]


class JWTData(BaseModel):
    user_id: uuid.UUID
    is_activated: bool


