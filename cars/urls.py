from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("car/<int:pk>/", views.car_detail, name="car_detail"),

    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),

    path("panel/", views.panel, name="panel"),
    path("panel/create/", views.panel_create, name="panel_create"),
    path("panel/edit/<int:pk>/", views.panel_edit, name="panel_edit"),
    path("panel/delete/<int:pk>/", views.panel_delete, name="panel_delete"),
    path("panel/avatar/", views.panel_avatar, name="panel_avatar"),
]
