from django import forms
from .models import CarListing, SiteSettings


class CarListingForm(forms.ModelForm):
    class Meta:
        model = CarListing
        fields = [
            "title", "year", "price", "mileage", "fuel_type",
            "drive_type", "city", "vin_code", "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название", "class": "field"}),
            "year": forms.NumberInput(attrs={"placeholder": "Год", "class": "field"}),
            "price": forms.NumberInput(attrs={"placeholder": "Цена", "class": "field"}),
            "mileage": forms.NumberInput(attrs={"placeholder": "Пробег", "class": "field"}),
            "fuel_type": forms.Select(attrs={"class": "field"}),
            "drive_type": forms.Select(attrs={"class": "field"}),
            "city": forms.TextInput(attrs={"placeholder": "Город", "class": "field"}),
            "vin_code": forms.TextInput(attrs={"placeholder": "VIN / код", "class": "field"}),
            "description": forms.Textarea(attrs={"placeholder": "Описание", "class": "field textarea", "rows": 8}),
        }


class MultiImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class CarImagesForm(forms.Form):
    photos = forms.FileField(
        required=False,
        widget=MultiImageInput(attrs={"multiple": True, "class": "field"}),
        label="Фото",
    )


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["site_name", "phone", "telegram", "avatar"]
