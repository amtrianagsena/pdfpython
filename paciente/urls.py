from django.urls import path
from .views import *

urlpatterns = [
    path('', PacienteListView.as_view(), name='paciente_list'),
    path('nuevo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('detalle/<int:pk>/', PacienteDetailView.as_view(), name='paciente_detail'),

    # 🔥 ESTA ES CLAVE PARA PDF
    path('<int:pk>/pdf/', generar_pdf_paciente, name='paciente_pdf'),
]