from django.db import models
from django.utils import timezone

from marketplaces.models import Marketplace, Country
from products.models import MarketplaceProduct

class OrderStatus(models.IntegerChoices):
    PROCESSING = 0, "Processing"
    PENDING = 1, "Pending"
    PREPARING = 2, "Preparing"
    SHIPPED = 3, "Shipped"
    REFUSED = 4, "Refused"
    CANCELED = 5, "Canceled"
    REFUNDED = 6, "Refunded"

class PayMethods(models.IntegerChoices):
    PAYPAL = 0, "PayPal"
    CREDIT_CARD = 1, "Credit Card"
    BANK_TRANSFER = 2, "Bank Transfer"
    CASH_ON_DELIVERY = 3, "Cash on Delivery"
    BIZUM = 4, "Bizum"

class Customer(models.Model):
    bill_phone = models.CharField(
        max_length=20,
    )
    bill_email = models.EmailField(
        max_length=255,
    )
    bill_firstname = models.CharField(
        max_length=50,
    )
    bill_lastname = models.CharField(
        max_length=50,
    )
    bill_company = models.CharField(
        max_length=100, 
        blank=True, 
        default="",
    )
    bill_address = models.CharField(
        max_length=255,
    )
    bill_city = models.CharField(
        max_length=100,
    )
    bill_zipcode = models.CharField(
        max_length=20,
    )
    bill_country = models.PositiveSmallIntegerField(
        choices=Country.choices,
    )
    ship_phone = models.CharField(
        max_length=20,
    )
    ship_email = models.EmailField(
        max_length=255,
    )
    ship_firstname = models.CharField(
        max_length=50,
    )
    ship_lastname = models.CharField(
        max_length=50,
    )
    ship_company = models.CharField(
        max_length=100,
        blank=True, 
        default="",
    )
    ship_address = models.CharField(
        max_length=255,
    )
    ship_city = models.CharField(
        max_length=100,
    )
    ship_zipcode = models.CharField(
        max_length=20,
    )
    ship_country = models.PositiveSmallIntegerField(
        choices=Country.choices,
    )

    def __str__(self):
        return f"{self.bill_firstname} {self.bill_lastname}"


class Carrier(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    marketplace =models.ForeignKey(
        Marketplace, 
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE
    )
    order_id = models.CharField(
        max_length=30,
    )
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING,
    )
    order_date = models.DateTimeField(
        default=timezone.now,
    )
    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.CASCADE,
    )
    ticket = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )
    ticket_refund = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )
    pay_method = models.PositiveSmallIntegerField(
        choices=PayMethods.choices
    )
    package_quantity = models.PositiveSmallIntegerField(
        default=1,
    )
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    notes = models.TextField(
        blank=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.order_id
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    marketplace_product = models.ForeignKey(
        MarketplaceProduct,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )