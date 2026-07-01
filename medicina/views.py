from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Medicina


class MedicinaListView(ListView):
    model = Medicina
    template_name = "medicina/list.html"
    context_object_name = "medicinas"


class MedicinaCreateView(CreateView):
    model = Medicina
    fields = ['nombre', 'descripcion']
    template_name = "medicina/form.html"
    success_url = reverse_lazy('medicina_list')


class MedicinaUpdateView(UpdateView):
    model = Medicina
    fields = ['nombre', 'descripcion']
    template_name = "medicina/form.html"
    success_url = reverse_lazy('medicina_list')


class MedicinaDeleteView(DeleteView):
    model = Medicina
    template_name = "medicina/delete.html"
    success_url = reverse_lazy('medicina_list')