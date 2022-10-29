from django.urls import path
from interfaces.views import index


urlpatterns = [
    path('', index, name='interfaces-home'),
]
