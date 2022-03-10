from django.urls import path
from .views import (UserView, userProfilView,
                    AddBons, EditView, addUser,
                    SearchResultsView, salaryProfilView,
                    AddFine, AddGive,EditSalaryView,
                    CalendarView, DateView)


urlpatterns = [
    path('users', UserView.as_view(), name='users'),
    path('usersprofil/<int:id>/', userProfilView, name='userprofil'),
    path('salaryprofil/<int:id>/', salaryProfilView, name='salaryprofil'),
    path('user/edit/<int:id>/', EditView.as_view(), name='edit_user'),
    path('user/salary/<int:id>/', EditSalaryView.as_view(), name='edit_salary'),
    path('add/bons/<int:id>/', AddBons.as_view(), name='addbons'),
    path('add/fine/<int:id>/', AddFine.as_view(), name='addfine'),
    path('add/give/<int:id>/', AddGive.as_view(), name='addgive'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('add/user/', addUser, name='adduser'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('date/<int:id>/', DateView.as_view(), name='date'),

]