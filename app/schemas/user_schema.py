from typing import Optional, List
from app.schemas.base_schema import BaseInfoModel, BaseList
from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    email: str
    is_activate: bool


class UserResponse(BaseInfoModel, UserInfo): ...


class UserListResponse(BaseList):
    results: Optional[List[UserResponse]]


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_activate: Optional[bool] = None


class UserCreateRequest(UserInfo): ...
