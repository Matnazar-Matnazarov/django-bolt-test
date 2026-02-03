from django_bolt import BoltAPI
from django.contrib.auth import get_user_model
from .schemas import UserSchema
from django.http import HttpRequest

User = get_user_model()

api = BoltAPI()


@api.get("/users/{user_id}")
async def get_user(request: HttpRequest, user_id: int) -> UserSchema:
    user = await User.objects.aget(id=user_id)
    return UserSchema.from_user(user)


@api.get("/users/")
async def get_users(request: HttpRequest) -> list[UserSchema]:
    users = await User.objects.all()
    return [UserSchema.from_user(user) for user in users]


@api.get("/users/me")
async def get_me(request: HttpRequest) -> UserSchema:
    user = await User.objects.aget(id=request.user.id)
    return UserSchema.from_user(user)
