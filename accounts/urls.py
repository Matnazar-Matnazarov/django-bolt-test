from django.urls import path
from . import views

urlpatterns = [
    path("users/<int:user_id>/", views.get_user, name="get_user"),
    path("users/", views.get_users, name="get_users"),
    path("users/me/", views.get_me, name="get_me"),
]