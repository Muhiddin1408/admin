from django.urls import path
from .views import UserView, userProfilView, AddBons, EditView


urlpatterns = [
    path('users', UserView.as_view(), name='users'),
    path('usersprofil/<int:id>/', userProfilView, name='userprofil'),
    path('user/edit/<int:id>/', EditView.as_view(), name='edit_user'),
    path('add/bons/<int:id>/', AddBons.as_view(), name='addbons'),
]