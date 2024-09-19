from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=0, source="unit_price"
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # serializing relationships

    # first Way String
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    # Second Way String
    collection = serializers.StringRelatedField()

    # Third Way Nested Objects
    # collection = CollectionSerializer()

    # fourth Way Hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="collection-detail"
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
