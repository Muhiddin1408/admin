from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View

from .models import Workers
from .forms import UserEditForm, AddBonsForm, AddUserForm, WorkersSearchForm, SalaryEditForm
# Create your views here.
from django.views.generic import ListView, UpdateView, CreateView, TemplateView


class UserView(TemplateView):
    model = Workers

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        context = super().get_context_data(**kwargs)
        context['users'] = Workers.objects.all()
        return render(request, 'admin/users.html', context)


def userProfilView(request, id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        user = Workers.objects.get(id=id)
        context = {
            'user': user
        }
        return render(request, 'admin/userprofil.html', context)


class EditView(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
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
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
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
        user.residue += int(form.data['bons'])
        user.save()
        return redirect(f'/api/admin/salaryprofil/{self.kwargs["id"]}/')

#
class AddUser(CreateView):
    queryset = Workers.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        form = AddUserForm
        context = {
            'form':form
        }
        return render(request, 'admin/adduser.html', context)

    def post(self, request, *args, **kwargs):
        form = AddUserForm(request.POST)
        if form.is_valid():

            user = Workers.objects.create(
                full_name=form.data['full_name'],
                telegram_id=form.data['telegram_id'],
                phone=form.data['phone'],
                job=form.data['shop'],
                age=form.data['age'],
                birthday=form.data['birthday'],
                # status=True

            )
            user.save()

            return redirect('users')


def addUser(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
    form = AddUserForm(request.POST)

    if request.method == "GET":
        form = AddUserForm
        context = {
            'form': form
        }
        return render(request, 'admin/adduser.html', context)
    if request.method == 'POST':
        user = Workers.objects.create(
            full_name=form.data['full_name'],
            telegram_id=form.data['telegram_id'],
            phone=form.data['phone'],
            job=form.data['shop'],
            age=form.data['age'],
            birthday=form.data['birthday'],

        )
        user.residue = user.salary+user.bons-user.fine-user.give
        user.save()
        return redirect('users')


# Search Salary




class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        query = self.request.GET.get('q')
        results = Workers.objects.filter(
        full_name=query
        )
        return render(request, 'admin/search.html', context={
        'title': 'Поиск',
        'result': results,
        })


def salaryProfilView(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('login'))
    user = Workers.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'admin/salaryprofil.html', context)


class EditSalaryView(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        form = SalaryEditForm
        user = Workers.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/salaryedit.html', context)

    def post(self, request, *args, **kwargs):
        form = SalaryEditForm(request.POST)
        user = Workers.objects.get(id=self.kwargs['id'])
        user.full_name = form.data['full_name']
        user.phone = form.data['phone']
        user.job = form.data['shop']
        user.salary = form.data['salary']

        user.residue = int(user.salary)+int(user.bons)-int(user.fine)-int(user.give)
        user.save()
        return HttpResponseRedirect(reverse_lazy('users'))


class AddFine(UpdateView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        form = AddBonsForm
        user = Workers.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/addfine.html', context)

    def post(self, request, *args, **kwargs):
        form = AddBonsForm(request.POST)
        user = Workers.objects.get(id=self.kwargs['id'])

        user.fine += int(form.data['fine'])
        user.residue -= int(form.data['five'])
        user.save()

        return redirect(f'/api/admin/salaryprofil/{self.kwargs["id"]}/')


class AddGive(UpdateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        form = AddBonsForm
        user = Workers.objects.get(id=self.kwargs['id'])
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'admin/addgive.html', context)

    def post(self, request, *args, **kwargs):
        form = AddBonsForm(request.POST)
        user = Workers.objects.get(id=self.kwargs['id'])

        user.give += int(form.data['give'])
        user.residue -= int(form.data['give'])
        user.save()

        return redirect(f'/api/admin/salaryprofil/{self.kwargs["id"]}/')


