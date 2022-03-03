from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import User
from .forms import UserEditForm, AddBonsForm
# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView


class UserView(ListView):
    model = User
    template_name = 'admin/users.html'
    queryset = User.objects.all()
    context_object_name = 'users'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['users'] = User.objects.all()
    #     return render(request, 'admin/userprofil.html', context)


def userProfilView(request, id):
    print(id)
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'admin/userprofil.html', context)


class EditView(UpdateView):
    def get(self, request, *args, **kwargs):
        form = UserEditForm
        user = User.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/useredit.html', context)

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST)
        user = User.objects.get(id=self.kwargs['id'])
        user.full_name = form.data['full_name']
        user.telegram_id = form.data['telegram_id']
        user.shop = form.data['shop']
        user.salary = form.data['salary']
        user.save()
        return HttpResponseRedirect(reverse_lazy('users'))


class AddBons(UpdateView):
    def get(self, request, *args, **kwargs):
        form = AddBonsForm
        user = User.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/addbons.html', context)

    def post(self, request, *args, **kwargs):
        form = AddBonsForm(request.POST)
        user = User.objects.get(id=self.kwargs['id'])

        user.bons += int(form.data['bons'])
        user.save()
        return HttpResponseRedirect(reverse_lazy('users'))