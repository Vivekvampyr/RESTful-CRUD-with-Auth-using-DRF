from rest_framework import serializers
from .models import Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "description",
            "price",
            "sale_price",
            "stock",
            "is_active",
            "owner",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        """Validate the regular price."""

        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value

    def validate(self, attrs):
        """Validate relationships between fields."""

        price = attrs.get(
            "price",
            getattr(self.instance, "price", None)
        )

        sale_price = attrs.get(
            "sale_price",
            getattr(self.instance, "sale_price", None)
        )

        # Normalize values before comparing them.
        if price is not None:
            price = Decimal(str(price))

        if sale_price is not None:
            sale_price = Decimal(str(sale_price))

        if (
            sale_price is not None
            and price is not None
            and sale_price >= price
        ):
            raise serializers.ValidationError({
                "sale_price": (
                    "Sale price must be lower than regular price."
                )
            })

        return attrs