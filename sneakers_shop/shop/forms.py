from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Введите имя',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Введите фамилию',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Фамилия'}),
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Введите адрес электронной почты',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Адрес электронной почты'}),
    )
    password1 = forms.CharField(
        help_text='Введите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=200,
        required=True,
        help_text='Эл. почта',
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'example@example.com'}),
    )
    password = forms.CharField(
        help_text='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Пароль'}),
    )

    class Meta:
        model = User
        fields = ('email', 'password')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_date']


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['reason', 'date']
