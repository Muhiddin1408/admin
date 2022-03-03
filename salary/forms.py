from django import forms
from .models import Workers


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ('full_name', 'telegram_id', 'job', 'salary', 'phone', 'birthday','age')


class AddBonsForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ('bons',)


class AddUserForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ('full_name', 'telegram_id', 'job', 'phone', 'birthday', 'age')


class WorkersSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Ism yoki familya buyicha qidiring!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )
