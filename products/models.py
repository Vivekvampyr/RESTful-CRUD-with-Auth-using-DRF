from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    sale_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,default=None)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name