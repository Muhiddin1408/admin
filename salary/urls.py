from django.urls import path
from .views import UserView, userProfilView, AddBons, EditView, addUser, SearchResultsView, salaryProfilView


urlpatterns = [
    path('users', UserView.as_view(), name='users'),
    path('usersprofil/<int:id>/', userProfilView, name='userprofil'),
    path('salaryprofil/<int:id>/', salaryProfilView, name='salaryprofil'),
    path('user/edit/<int:id>/', EditView.as_view(), name='edit_user'),
    path('add/bons/<int:id>/', AddBons.as_view(), name='addbons'),
    path('add/fine/<int:id>/', AddBons.as_view(), name='addfine'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('add/user/', addUser, name='adduser'),
]