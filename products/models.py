from django.db import models
from django.core.exceptions import ValidationError

from marketplaces.models import Marketplace

class DataType(models.IntegerChoices):
    INT = 1
    DECIMAL = 2
    STRING = 3
    TEXT = 4
    DATE = 5
    DATETIME = 6
    BOOLEAN = 7

class Product(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(
        max_length=250,
    )
    sku = models.CharField(
        max_length=50,
    )
    reference = models.CharField(
        max_length=50,
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField()
    image = models.URLField(
        null=True,
    )

    def __str__(self):
        return self.sku

class MarketplaceProduct(models.Model):
    marketplace = models.ForeignKey(
        Marketplace,
        on_delete=models.CASCADE,
        related_name="marketplace_products",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    enabled = models.BooleanField(
        default=True,
    )

    def clean(self):
        if self.product.children.exists():
            raise ValidationError("A product with children cannot be associated with a marketplace")
        
    def __str__(self):
        return f"{self.marketplace} - {self.product.sku}"

class Attribute(models.Model):
    
    data_type = models.PositiveSmallIntegerField(
        choices=DataType.choices,
    )
    data_int = models.IntegerField(
        null=True,
        blank=True,
    )
    data_decimal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    data_string = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    data_text = models.TextField(
        null=True,
        blank=True,
    )
    data_date = models.DateField(
        null=True,
        blank=True,
    )
    data_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    data_boolean = models.BooleanField(
        null=True,
        blank=True,
    )

    class Meta():
        abstract = True
        constraints = [
            models.CheckConstraint(
                name='unique_value_type_field_%(class)s',
                check=(
                    models.Q(
                        data_type=DataType.INT,
                        data_int__isnull=False,
                        data_decimal__isnull=True,
                        data_string__isnull=True,
                        data_text="",
                        data_date__isnull=True,
                        data_datetime__isnull=True,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.DECIMAL,
                        data_int__isnull=True,
                        data_decimal__isnull=False,
                        data_string__isnull=True,
                        data_text="",
                        data_date__isnull=True,
                        data_datetime__isnull=True,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.STRING,
                        data_int__isnull=True,
                        data_decimal__isnull=True,
                        data_string__isnull=False,
                        data_text="",
                        data_date__isnull=True,
                        data_datetime__isnull=True,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.TEXT,
                        data_int__isnull=True,
                        data_decimal__isnull=True,
                        data_string__isnull=True,
                        data_text__gt="",
                        data_date__isnull=True,
                        data_datetime__isnull=True,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.DATE,
                        data_int__isnull=True,
                        data_decimal__isnull=True,
                        data_string__isnull=True,
                        data_text="",
                        data_date__isnull=False,
                        data_datetime__isnull=True,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.DATETIME,
                        data_int__isnull=True,
                        data_decimal__isnull=True,
                        data_string__isnull=True,
                        data_text="",
                        data_date__isnull=True,
                        data_datetime__isnull=False,
                        data_boolean__isnull=True,
                    )
                    | models.Q(
                        data_type=DataType.BOOLEAN,
                        data_int__isnull=True,
                        data_decimal__isnull=True,
                        data_string__isnull=True,
                        data_text="",
                        data_date__isnull=True,
                        data_datetime__isnull=True,
                        data_boolean__isnull=False,
                    )
                )
            )
        ]

    def clean(self):
        data_type_names = {
            DataType.INT: "Integer",
            DataType.DECIMAL: "Decimal",
            DataType.STRING: "String",
            DataType.TEXT: "Text",
            DataType.DATE: "Date",
            DataType.DATETIME: "Datetime",
            DataType.BOOLEAN: "Boolean",
        }
        data_fields = {
            DataType.INT: self.data_int,
            DataType.DECIMAL: self.data_decimal,
            DataType.STRING: self.data_string,
            DataType.TEXT: self.data_text,
            DataType.DATE: self.data_date,
            DataType.DATETIME: self.data_datetime,
            DataType.BOOLEAN: self.data_boolean,
        }

        if not any(data_fields.values()):
            raise ValidationError("At least one field must be filled")

        if self.data_type in data_fields and not data_fields[self.data_type]:
            field_name = data_type_names.get(self.data_type, "Unknown")
            raise ValidationError(f"The {field_name} field must be filled")
        
class AttributeType(models.Model):
    name = models.CharField(
        max_length=75,
    )
    data_type = models.PositiveSmallIntegerField(
        choices=DataType.choices,
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

class ProductAttributeType(AttributeType):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_name",
                fields=["name"],
            )
        ]

    def clean(self):
        if ProductAttributeType.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError("This name is already in use")
        
    def __str__(self):
        return self.name
        
class ProductAttribute(Attribute):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attributes",
    )
    attribute_type = models.ForeignKey(
        ProductAttributeType,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = Attribute.Meta.constraints + [
            models.UniqueConstraint(
                fields=["product", "attribute_type"],
                name="unique_product_attribute",
            )
        ]

    def clean(self):
        super().clean()
        if self.attribute_type.data_type != self.data_type:
            raise ValidationError("The data type of the attribute does not match the data type of the attribute type")
        if ProductAttribute.objects.filter(product=self.product, attribute_type=self.attribute_type).exclude(pk=self.pk).exists():
            raise ValidationError("This attribute type is already associated with this product")
        
    def __str__(self):
        return f"{self.product.sku} - {self.attribute_type.name}"