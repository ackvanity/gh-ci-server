from django.urls import path
from . import views

urlpatterns = [
    path("callbacks/<uuid:id>", views.webhook, name="index"),
]
