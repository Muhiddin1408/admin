from django import forms
from .models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'telegram_id', 'shop', 'salary')


class AddBonsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bons',)
