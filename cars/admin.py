from django.contrib import admin
from .models import CarListing, CarImage, SiteSettings


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "year", "price", "mileage", "fuel_type", "drive_type", "city", "is_active", "created_at")
    list_filter = ("brand", "fuel_type", "drive_type", "city", "is_active", "year")
    search_fields = ("title", "brand", "vin_code", "city")
    inlines = [CarImageInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass
