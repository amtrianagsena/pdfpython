from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

from .models import Paciente

import os
from datetime import datetime


# 🔍 LIST + SEARCH
class PacienteListView(ListView):
    model = Paciente
    template_name = "paciente/list.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Paciente.objects.filter(nombre__icontains=query)
        return Paciente.objects.all()


# ➕ CREATE
class PacienteCreateView(CreateView):
    model = Paciente
    fields = ['nombre', 'documento', 'fecha_nacimiento', 'medicinas']
    template_name = "paciente/form.html"
    success_url = reverse_lazy('paciente_list')


# ✏️ UPDATE
class PacienteUpdateView(UpdateView):
    model = Paciente
    fields = ['nombre', 'documento', 'fecha_nacimiento', 'medicinas']
    template_name = "paciente/form.html"
    success_url = reverse_lazy('paciente_list')


# ❌ DELETE
class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = "paciente/delete.html"
    success_url = reverse_lazy('paciente_list')


# 👁 DETAIL
class PacienteDetailView(DetailView):
    model = Paciente
    template_name = "paciente/detail.html"


# 📄 PDF
def generar_pdf_paciente(request, pk):
    paciente = get_object_or_404(Paciente, id=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receta_{paciente.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # 🖼 LOGO
    logo_path = os.path.join(settings.BASE_DIR, "static/img/logo.png")
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 40, height - 100, width=80, height=80)

    # 🏥 ENCABEZADO
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, height - 50, "CLÍNICA MÉDICA - RECETA MÉDICA")

    p.setStrokeColor(colors.black)
    p.line(40, height - 110, 570, height - 110)

    # 📅 FECHA
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    p.setFont("Helvetica", 10)
    p.drawString(450, height - 130, f"Fecha: {fecha}")

    # 👤 DATOS PACIENTE
    y = height - 170
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "DATOS DEL PACIENTE")
    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Nombre: {paciente.nombre}")
    y -= 15
    p.drawString(40, y, f"Documento: {paciente.documento}")
    y -= 15
    p.drawString(40, y, f"Fecha nacimiento: {paciente.fecha_nacimiento}")

    # 💊 MEDICAMENTOS
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "MEDICAMENTOS RECETADOS")
    y -= 25

    # 🧾 TABLA SIMPLIFICADA
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "N°")
    p.drawString(100, y, "Medicamento")
    p.drawString(350, y, "Descripción")
    y -= 15

    p.line(40, y, 570, y)
    y -= 20

    p.setFont("Helvetica", 10)

    for i, m in enumerate(paciente.medicinas.all(), start=1):
        if y < 100:
            p.showPage()
            y = height - 100

        p.drawString(50, y, str(i))
        p.drawString(100, y, m.nombre[:30])
        p.drawString(350, y, (m.descripcion[:40] if m.descripcion else "-"))
        y -= 20

    # 🧾 FIRMA
    y -= 60
    p.line(400, y, 550, y)
    p.drawString(420, y - 15, "Firma del médico")

    # 🏁 FINAL
    p.showPage()
    p.save()

    return response