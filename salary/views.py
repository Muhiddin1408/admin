from django.shortcuts import render
from .models import User
# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView


class User(ListView):
    model = User
    template_name = 'admin/users.html'
    queryset = User.objects.all()
    context_object_name = 'users'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['users'] = User.objects.all()
    #     return render(request, 'admin/userprofil.html', context)

class UserProfilView(TemplateView):
    model = User
    template_name = 'admin/userprofil.html'
    queryset = User.objects.all()
    context_object_name = 'users'
