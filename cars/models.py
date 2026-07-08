from django.db import models


class SiteSettings(models.Model):
    """Singleton-style model holding the global site info (logo, contacts, avatar)."""
    site_name = models.CharField(max_length=100, default="AUTOUA")
    phone = models.CharField(max_length=30, default="+380000000000")
    telegram = models.CharField(max_length=100, default="@username",
                                 help_text="Telegram username, with or without @")
    tiktok = models.CharField(max_length=100, blank=True,
                               help_text="Ссылка на TikTok или @username")
    instagram = models.CharField(max_length=100, blank=True,
                                  help_text="Ссылка на Instagram или @username")
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def telegram_url(self):
        handle = self.telegram.lstrip("@").strip()
        return f"https://t.me/{handle}"

    @property
    def phone_url(self):
        digits = "".join(ch for ch in self.phone if ch.isdigit() or ch == "+")
        return f"tel:{digits}"

    @property
    def tiktok_url(self):
        value = (self.tiktok or "").strip()
        if not value:
            return ""
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return f"https://www.tiktok.com/@{value.lstrip('@')}"

    @property
    def instagram_url(self):
        value = (self.instagram or "").strip()
        if not value:
            return ""
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return f"https://www.instagram.com/{value.lstrip('@')}"

    def __str__(self):
        return self.site_name


FUEL_CHOICES = [
    ("Бензин", "Бензин"),
    ("Дизель", "Дизель"),
    ("Газ/Бензин", "Газ/Бензин"),
    ("Гибрид", "Гибрид"),
    ("Электро", "Электро"),
]

DRIVE_CHOICES = [
    ("Передний привод", "Передний привод"),
    ("Задний привод", "Задний привод"),
    ("Полный привод", "Полный привод"),
]

BRAND_CHOICES = [
    ("Audi", "Audi"),
    ("BMW", "BMW"),
    ("Chevrolet", "Chevrolet"),
    ("Citroen", "Citroen"),
    ("Fiat", "Fiat"),
    ("Ford", "Ford"),
    ("Honda", "Honda"),
    ("Hyundai", "Hyundai"),
    ("Kia", "Kia"),
    ("Lexus", "Lexus"),
    ("Mazda", "Mazda"),
    ("Mercedes-Benz", "Mercedes-Benz"),
    ("Mitsubishi", "Mitsubishi"),
    ("Nissan", "Nissan"),
    ("Opel", "Opel"),
    ("Peugeot", "Peugeot"),
    ("Renault", "Renault"),
    ("Skoda", "Skoda"),
    ("Subaru", "Subaru"),
    ("Suzuki", "Suzuki"),
    ("Toyota", "Toyota"),
    ("Volkswagen", "Volkswagen"),
    ("Volvo", "Volvo"),
    ("Другое", "Другое"),
]


class CarListing(models.Model):
    brand = models.CharField(max_length=60, choices=BRAND_CHOICES, default="BMW", verbose_name="Марка")
    title = models.CharField(max_length=150, verbose_name="Название")
    year = models.PositiveIntegerField(verbose_name="Год")
    price = models.PositiveIntegerField(verbose_name="Цена ($)")
    mileage = models.PositiveIntegerField(verbose_name="Пробег (км)")
    fuel_type = models.CharField(max_length=30, choices=FUEL_CHOICES, default="Бензин", verbose_name="Топливо")
    drive_type = models.CharField(max_length=30, choices=DRIVE_CHOICES, default="Передний привод", verbose_name="Привод")
    city = models.CharField(max_length=80, verbose_name="Город")
    vin_code = models.CharField(max_length=40, blank=True, verbose_name="VIN / код")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.title} ({self.year})"

    @property
    def main_image(self):
        first = self.images.first()
        return first.image.url if first else None


class CarImage(models.Model):
    listing = models.ForeignKey(CarListing, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cars/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image for {self.listing_id}"
