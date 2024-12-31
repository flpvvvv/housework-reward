from django.urls import path
from . import views

urlpatterns = [
    path('record/add/', views.add_housework_record, name='add_housework_record'),
    path('contributors/add/', views.add_contributor, name='add_contributor'),
    path('contributors/<int:pk>/update/', views.update_contributor, name='update_contributor'),
    path('contributors/<int:pk>/delete/', views.delete_contributor, name='delete_contributor'),
]
