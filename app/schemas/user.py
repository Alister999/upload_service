from pydantic import BaseModel

class BaseUser(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseUser):
    username: str
    password: str


class UserLogin(BaseUser):
    username: str
    password: str

class UserResponse(BaseUser):
    username: str
    password_hash: str


class RefreshToken(BaseUser):
    refresh_token: str