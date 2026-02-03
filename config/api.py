from django_bolt import BoltAPI
from django.contrib.auth import get_user_model
from accounts.schemas import UserSchema
from django.http import HttpRequest, JsonResponse

from config.middleware import ServerTimeMiddleware

User = get_user_model()

api = BoltAPI(middleware=[ServerTimeMiddleware])


@api.get("/users/{user_id}")
async def get_user(request: HttpRequest, user_id: int) -> UserSchema:
    user = await User.objects.only("id", "username").aget(id=user_id)
    return UserSchema.from_user(user)


@api.get("/users/")
async def get_users(request: HttpRequest) -> list[UserSchema]:
    users = []
    async for user in User.objects.only("id", "username"):
        users.append(user)
    return [UserSchema.from_user(u) for u in users]


@api.get("/users/me")
async def get_me(request: HttpRequest):
    if not (request.user and request.user.is_authenticated):
        return JsonResponse({"detail": "Authentication required"}, status=401)
    user = await User.objects.only("id", "username").aget(id=request.user.id)
    return UserSchema.from_user(user)