from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


def say_hello(request):
    products = Product.objects.all()

    for product in products:
        print(product)
    return render(request, "hello.html", {"name": "Mosh"})
