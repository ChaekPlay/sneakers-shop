from django import forms
from .models import *


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Client.user
        fields = ['firstName', 'lastName', 'email', 'phone']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_date']


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['reason', 'date']