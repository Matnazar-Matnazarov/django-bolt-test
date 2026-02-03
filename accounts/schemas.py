import msgspec
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# User schema for Bolt API
class UserSchema(msgspec.Struct):
    id: int
    username: str

    @classmethod
    def from_user(cls, user: User) -> "UserSchema":
        return cls(id=user.id, username=user.username)


# User schema for Django Admin
class UserAdminSchema(msgspec.Struct):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: timezone.datetime

    @classmethod
    def from_user(cls, user: User) -> "UserAdminSchema":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            last_login=user.last_login or timezone.now(),
        )
