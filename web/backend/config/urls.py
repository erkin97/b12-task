from django.urls import path
from flights.api import api

urlpatterns = [
    path("api/", api.urls),
]
