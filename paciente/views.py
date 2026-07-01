from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.pdfgen import canvas
from .models import Paciente


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
    response['Content-Disposition'] = f'attachment; filename="paciente_{paciente.nombre}.pdf"'

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "RECETA MÉDICA / MEDICAMENTOS")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Paciente: {paciente.nombre}")
    y -= 20
    p.drawString(100, y, f"Documento: {paciente.documento}")
    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Medicamentos:")
    y -= 20

    p.setFont("Helvetica", 12)

    for m in paciente.medicinas.all():
        p.drawString(120, y, f"- {m.nombre}")
        y -= 20

        if y < 100:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    return response