from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer, UserRetrieveSerializer, UserListSerializer, UserCreateSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "me":
            return UserRetrieveSerializer
        elif self.action == "list":
            return UserListSerializer
        elif self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        return [AllowAny()]

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        user = get_object_or_404(queryset)
        serializer = self.get_serializer(user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def activate_by_email(self, request):
        """Активация пользователя СуперАдмином"""
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email was not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.user.is_superuser:
            user.is_active = True
            user.save()
            return Response({"message": "User activated."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You do not have rights to activate the user."},
                status=status.HTTP_403_FORBIDDEN,
            )
