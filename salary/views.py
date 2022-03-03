from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Workers
from .forms import UserEditForm, AddBonsForm, AddUserForm
# Create your views here.
from django.views.generic import ListView, UpdateView, CreateView


class UserView(ListView):
    model = Workers
    template_name = 'admin/users.html'
    queryset = Workers.objects.all()
    context_object_name = 'users'


def userProfilView(request, id):
    user = Workers.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'admin/userprofil.html', context)


class EditView(UpdateView):
    def get(self, request, *args, **kwargs):
        form = UserEditForm
        user = Workers.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/useredit.html', context)

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST)
        user = Workers.objects.get(id=self.kwargs['id'])
        user.full_name = form.data['full_name']
        user.telegram_id = form.data['telegram_id']
        user.phone = form.data['phone']
        user.job = form.data['shop']
        user.age = form.data['age']
        user.birthday = form.data['birthday']
        user.save()
        return HttpResponseRedirect(reverse_lazy('users'))


class AddBons(UpdateView):
    def get(self, request, *args, **kwargs):
        form = AddBonsForm
        user = Workers.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/addbons.html', context)

    def post(self, request, *args, **kwargs):
        form = AddBonsForm(request.POST)
        user = Workers.objects.get(id=self.kwargs['id'])

        user.bons += int(form.data['bons'])
        user.save()
        return HttpResponseRedirect(reverse_lazy('users'))

#
# class AddUser(CreateView):
#     queryset = Workers.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         form = AddUserForm
#         context = {
#             'form':form
#         }
#         return render(request, 'admin/adduser.html')
#
#     def post(self, request, *args, **kwargs):
#         form = AddUserForm(request.POST)
#         print(form.data)
#         if form.is_valid():
#             print('hello')
#             user = Workers.objects.create(
#                 full_name=form.data['full_name'],
#                 telegram_id=form.data['telegram_id'],
#                 phone=form.data['phone'],
#                 job=form.data['shop'],
#                 age=form.data['age'],
#                 birthday=form.data['birthday'],
#
#             )
#             user.save()
#             print('salom')
#             return HttpResponseRedirect(reverse_lazy('adduser'))

def addUser(request):
    form = AddUserForm(request.POST)
    if request.method == 'POST':
        print('hello')
        user = Workers.objects.create(
            full_name=form.data['full_name'],
            telegram_id=form.data['telegram_id'],
            phone=form.data['phone'],
            job=form.data['shop'],
            age=form.data['age'],
            birthday=form.data['birthday'],

        )
        user.save()
        return redirect('users')

