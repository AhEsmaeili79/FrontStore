from ast import mod
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from tags.models import TaggedItem


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low"), (">10", "OK")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class Taginline(GenericTabularInline):
    model = TaggedItem


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    inlines = [Taginline]
    list_display = ["title", "unit_price", "inventory_status", "collection__title"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_per_page = 10
    search_fields = ["title"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f"{updated_count} products updated")


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        # reverse("admin_app_model_page")
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a  href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "order_counts"]
    list_editable = ["membership"]
    list_per_page = 10
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="order_counts")
    def order_counts(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.order_counts)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_counts=Count("order"))


class orderItemInline(admin.StackedInline):
    autocomplete_fields = ["product"]
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "placed_at", "payment_status"]
    ordering = ["placed_at"]
    list_select_related = ["customer"]
    inlines = [orderItemInline]
    list_per_page = 10
    autocomplete_fields = ["customer"]
