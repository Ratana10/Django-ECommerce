from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms import  TextInput, EmailInput, Select, FileInput
from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User name')
    email = forms.EmailField(max_length=200, label='Email')
    first_name = forms.CharField(max_length=100, help_text='First Name' ,label='First name')
    last_name = forms.CharField(max_length=100, help_text='Last Name' ,label='Last name')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'Username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'Email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'First Name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'Last Name' }),
        }
        

CITY = [
    ('Phnom Penh', 'Phnom Penh'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image',)
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'Phone'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'Address'}),
            'city'      : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input','placeholder':'Country' }),
            'image'     : FileInput(attrs={ 'placeholder': 'image', }),
        }


