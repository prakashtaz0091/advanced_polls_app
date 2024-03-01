from django.urls import path
from . import views

app_name = 'advanced_polls_app'

urlpatterns = [
    path('', views.home, name='home'),
]