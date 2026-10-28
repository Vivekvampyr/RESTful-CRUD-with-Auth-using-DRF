from django.db import transaction

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from .auth_serializers import (
    RegisterSerializer,
    RegistrationResponseSerializer,
    TokenResponseSerializer,
)


class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegistrationResponseSerializer},
        auth=[],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "id": user.pk,
                "username": user.get_username(),
                "email": user.email,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @extend_schema(
        request={"application/json": AuthTokenSerializer},
        responses={200: TokenResponseSerializer},
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)