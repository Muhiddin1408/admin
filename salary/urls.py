from django.urls import path
from .views import User


urlpatterns = [
    path('users', User.as_view(), name='users'),
    path('usersprofil/<int:id>/', User.as_view(), name='userprofil')
]