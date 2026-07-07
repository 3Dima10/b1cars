from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CarListingForm, SiteSettingsForm
from .models import CarListing, CarImage, SiteSettings


def is_admin(user):
    return user.is_authenticated and user.is_staff


def site_context():
    return {"settings": SiteSettings.load()}


def home(request):
    cars = CarListing.objects.filter(is_active=True).prefetch_related("images")
    context = {"cars": cars, **site_context()}
    return render(request, "cars/index.html", context)


def car_detail(request, pk):
    car = get_object_or_404(CarListing, pk=pk, is_active=True)
    context = {"car": car, **site_context()}
    return render(request, "cars/detail.html", context)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("panel")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("panel")
        error = "Неверный логин или пароль"

    return render(request, "cars/admin_login.html", {"error": error, **site_context()})


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    return redirect("home")


@user_passes_test(is_admin, login_url="admin_login")
def panel(request):
    mode = request.GET.get("mode", "")
    cars = CarListing.objects.all().prefetch_related("images")
    form = CarListingForm()

    context = {
        "cars": cars,
        "mode": mode,
        "form": form,
        "edit_car": None,
        **site_context(),
    }
    return render(request, "cars/admin_panel.html", context)


@user_passes_test(is_admin, login_url="admin_login")
def panel_create(request):
    if request.method == "POST":
        form = CarListingForm(request.POST)
        if form.is_valid():
            car = form.save()
            for i, f in enumerate(request.FILES.getlist("photos")):
                CarImage.objects.create(listing=car, image=f, order=i)
            messages.success(request, "Объявление создано")
            return redirect("panel")
    else:
        form = CarListingForm()

    context = {
        "cars": CarListing.objects.all().prefetch_related("images"),
        "mode": "create",
        "form": form,
        "edit_car": None,
        **site_context(),
    }
    return render(request, "cars/admin_panel.html", context)


@user_passes_test(is_admin, login_url="admin_login")
def panel_edit(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    if request.method == "POST":
        form = CarListingForm(request.POST, instance=car)
        if form.is_valid():
            form.save()

            # Remove photos the user checked for deletion. Deleting the
            # CarImage rows also deletes the actual files from disk
            # (see cars/signals.py).
            delete_ids = request.POST.getlist("delete_photos")
            if delete_ids:
                CarImage.objects.filter(listing=car, id__in=delete_ids).delete()

            # Append any newly uploaded photos after the existing ones.
            new_files = request.FILES.getlist("photos")
            if new_files:
                next_order = (car.images.aggregate(m=Max("order"))["m"] or 0) + 1
                for i, f in enumerate(new_files):
                    CarImage.objects.create(listing=car, image=f, order=next_order + i)

            messages.success(request, "Объявление обновлено")
            return redirect("panel")
    else:
        form = CarListingForm(instance=car)

    context = {
        "cars": CarListing.objects.all().prefetch_related("images"),
        "mode": "edit-form",
        "form": form,
        "edit_car": car,
        **site_context(),
    }
    return render(request, "cars/admin_panel.html", context)


@user_passes_test(is_admin, login_url="admin_login")
@require_POST
def panel_delete(request, pk):
    car = get_object_or_404(CarListing, pk=pk)
    car.delete()
    messages.success(request, "Объявление удалено")
    return redirect("panel")


@user_passes_test(is_admin, login_url="admin_login")
@require_POST
def panel_avatar(request):
    settings_obj = SiteSettings.load()
    form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
    if form.is_valid():
        form.save()
    return redirect("panel")
