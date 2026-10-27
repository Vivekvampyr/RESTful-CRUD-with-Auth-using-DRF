from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny


class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)