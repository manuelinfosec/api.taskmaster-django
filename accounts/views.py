from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response

from accounts.services import AuthService
from taskmaster.permissions import IsAuthenticated, IsObjectOwner
from taskmaster.utils import get_object_or_error

auth_service = AuthService()


class RegisterAPI(generics.GenericAPIView):
    def post(self, request):
        return Response(
            data=auth_service.register_user(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                username=request.data.get("username"),
                email=request.data.get("email"),
                password=request.data.get("password"),
            ),
            status=status.HTTP_201_CREATED,
        )


class LoginAPI(generics.GenericAPIView):
    def post(self, request):
        return Response(
            data=auth_service.login_user(
                username=request.data.get("username"),
                password=request.data.get("password"),
            ),
            status=status.HTTP_200_OK,
        )


class ProfileAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_object(self):
        obj = get_object_or_error(get_user_model(), id=self.request.user.id)
        self.check_object_permissions(self.request, obj.id)

        obj = auth_service.get_user(user_id=obj.id)
        return obj

    def get(self, request):
        return Response(
            data=auth_service.get_user(
                user_id=request.user.id,
                auth_provider=request.user.auth_provider,
                auth_provider_id=request.user.auth_provider_id,
            ),
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        self.get_object()

        return Response(
            data=auth_service.update_user(
                user_id=request.user.id,
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                username=request.data.get("username"),
                email=request.data.get("email"),
                phone_number=request.data.get("phone_number"),
                user_type=request.data.get("user_type"),
            ),
            status=status.HTTP_202_ACCEPTED,
        )


class UserUpdatePasswordAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            data=auth_service.update_user_password(
                user_id=request.user.id,
                old_password=request.data.get("old_password"),
                new_password_1=request.data.get("new_password_1"),
                new_password_2=request.data.get("new_password_2"),
            ),
            status=status.HTTP_200_OK,
        )
