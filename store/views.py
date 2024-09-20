from msilib.schema import SelfReg
from unittest.util import safe_repr
from urllib import request, response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Product, Collection
from rest_framework.views import APIView
from .serializers import CollectionSerializer, ProductSerializer
from rest_framework import status
from django.db.models import Count


class ProductList(APIView):

    def get(self, request):
        products = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):

    def get(self, request):
        collection = Collection.objects.annotate(proudcts_count=Count("products")).all()
        serializer = CollectionSerializer(collection, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):

    def get(self, request):
        collection = get_object_or_404(
            Collection.objects.annotate(proudcts_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def post(self, request):
        collection = get_object_or_404(
            Collection.objects.annotate(proudcts_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        collection = get_object_or_404(
            Collection.objects.annotate(proudcts_count=Count("products")), pk=pk
        )
        if collection.products.count() > 0:
            return Response(
                {
                    "error": f"you can not delete {collection.title} this collection includes some of products."
                }
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def product_list(request):
#     if request.method == "GET":
#         products = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(
#             products, many=True, context={"request": request}
#         )
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(data=request.data)

#         # we can use this or
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# we can use this both do same things

# if serializer.is_valid():
#     serializer.save()
#     return Response("ok")
# else:
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
