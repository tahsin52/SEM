from django.db import models


class CarModel(models.Model):
    bodystyle = models.CharField(max_length=155, null=True)
    canonical_mmt = models.CharField(max_length=155, null=True)
    customer_id = models.CharField(max_length=155, null=True)
    fuel_type = models.CharField(max_length=155, null=True)
    listing_id = models.CharField(max_length=155, null=True)
    make = models.CharField(max_length=155, null=True)
    mileage = models.CharField(max_length=155, null=True)
    model = models.CharField(max_length=155, null=True)
    msrp = models.CharField(max_length=155, null=True)
    price = models.CharField(max_length=155, null=True)
    seller_type = models.CharField(max_length=155, null=True)
    stock_type = models.CharField(max_length=155, null=True)
    trim = models.CharField(max_length=155, null=True)
    vin = models.CharField(max_length=155, null=True)
    year = models.CharField(max_length=155, null=True)
    exterior_color = models.CharField(max_length=155, null=True)
    transmission = models.CharField(max_length=155, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.model)
