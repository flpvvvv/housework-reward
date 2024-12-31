from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_housework_record, name='add_housework_record'),
]
