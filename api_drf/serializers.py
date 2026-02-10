"""DRF serializers."""

from rest_framework import serializers

from accounts.models import Role
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User response (id, username, role)."""

    class Meta:
        model = User
        fields = ("id", "username", "role")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = getattr(instance, "role", None) or Role.CUSTOMER
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    """Create user with role."""

    class Meta:
        model = User
        fields = ("username", "password", "email", "role")

    def create(self, validated_data):
        role = validated_data.pop("role", Role.CUSTOMER)
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
        )
        user.role = role
        user.save(update_fields=["role"])
        return user
