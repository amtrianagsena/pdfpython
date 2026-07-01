from django.urls import path
from .views import *

urlpatterns = [
    path('', MedicinaListView.as_view(), name='medicina_list'),
    path('nuevo/', MedicinaCreateView.as_view(), name='medicina_create'),
    path('editar/<int:pk>/', MedicinaUpdateView.as_view(), name='medicina_update'),
    path('eliminar/<int:pk>/', MedicinaDeleteView.as_view(), name='medicina_delete'),
]