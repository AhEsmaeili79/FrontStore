from rest_framework.response import Response
from .models import OrderItem, Product, Collection
from .serializers import CollectionSerializer, ProductSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {"error": f"you can not delete this product includes some of orders."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(proudcts_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": f"you can not delete this collection includes some of products."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


# we can use ListCreateAPIView if we have logics
# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related("collection").all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def get_serializer_context(self):
#         return {"request": self.request}


# or we can use API_VIEW
# class ProductList(APIView):
# def get(self, request):
#     products = Product.objects.select_related("collection").all()
#     serializer = ProductSerializer(
#         products, many=True, context={"request": request}
#     )
#     return Response(serializer.data)

# def post(self, request):
#     serializer = ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     print(serializer.validated_data)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


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
