from django.contrib import admin
from .models import CarListing, CarImage, SiteSettings


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(CarListing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "price", "city", "is_active", "created_at")
    inlines = [CarImageInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass
