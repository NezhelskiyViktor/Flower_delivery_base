from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class LoginByEmailForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email