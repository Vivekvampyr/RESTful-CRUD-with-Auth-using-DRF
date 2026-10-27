from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    sale_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,default=None,validators=[MinValueValidator(Decimal("0.01"))])
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=Q(price__gt=0),
                name="prd_price_gt_zero",
            ),
            models.CheckConstraint(
                condition=(
                    Q(sale_price__isnull=True)
                    | Q(sale_price__gt=0)
                ),
                name="prd_sale_gt_zero",
            ),
            models.CheckConstraint(
                condition=(
                    Q(sale_price__isnull=True)
                    | Q(sale_price__lt=F("price"))
                ),
                name="prd_sale_lt_price",
            ),
        ]
    
    def __str__(self):
        return self.name