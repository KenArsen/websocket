from rest_framework import serializers

from user.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
        ref_name = "UserList"


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "last_login",
            "is_superuser",
        )
        ref_name = "UserRetrieve"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")
        ref_name = "User"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "phone_number",
            "first_name",
            "last_name",
            "role",
        )
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}
        ref_name = "UserCreate"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
