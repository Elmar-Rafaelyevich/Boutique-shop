from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from shop.models import *

# Для входа 
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control', 
                   'placeholder':'Имя пользователя'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 
                   'placeholder':'Пароль'}))

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        label='Имя пользователя'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}),
        label='Электронная почта'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# comment form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'grade')
        widgets = {'text': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ваш отзыв...'}),
                   'grade': forms.Select(attrs={'class':'form-control', 'placeholder':'Ваш оценка...'})}