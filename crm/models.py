from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal
import uuid


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$|^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be entered in the format: '+999999999' or '999-999-9999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        ordering = ['name']


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_amount(self):
        """Calculate total amount based on associated products"""
        total = sum(product.price for product in self.products.all())
        self.total_amount = total
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:  # Only calculate if order exists (for M2M relationship)
            self.calculate_total_amount()
            super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - ${self.total_amount}"

    class Meta:
        ordering = ['-order_date']


