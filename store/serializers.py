from dataclasses import fields
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=0)
