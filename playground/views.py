from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import OrderItem, Product


def say_hello(request):

    products = Product.objects.filter(
        id__in=OrderItem.objects.values("product__id").distinct()
    ).order_by("title")
    context = {
        "products": list(products),
    }
    return render(request, "hello.html", context)
