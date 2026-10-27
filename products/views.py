from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsProductOwner

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticated,
        IsProductOwner,
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Product.objects.none()
        return Product.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)