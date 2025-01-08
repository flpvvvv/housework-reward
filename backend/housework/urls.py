from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.list_housework_records, name='list_housework_records'),
    path('records/add/', views.add_housework_record, name='add_housework_record'),
    path('records/<int:pk>/update/', views.update_housework_record, name='update_housework_record'),
    path('records/<int:pk>/delete/', views.delete_housework_record, name='delete_housework_record'),
    path('contributors/add/', views.add_contributor, name='add_contributor'),
    path('contributors/<int:pk>/update/', views.update_contributor, name='update_contributor'),
    path('contributors/<int:pk>/delete/', views.delete_contributor, name='delete_contributor'),
]
