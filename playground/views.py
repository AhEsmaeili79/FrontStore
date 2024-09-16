from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    query_set = Product.objects.get(pk=1)

    return render(request, "hello.html", {"name": "Mosh"})
