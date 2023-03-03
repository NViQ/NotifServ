from django.urls import path
from .views import *


urlpatterns = [
    # path('', index),
    path('client/', Client.as_view()),
    path('mailings/', Mailings.as_view()),
]