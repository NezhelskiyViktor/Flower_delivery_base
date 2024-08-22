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
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
        error_messages={'required': 'Это поле обязательно для заполнения.'}
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой не найден.')
        return email


class LoginByEmailForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email


class DeliveryAddressForm(forms.Form):
    address = forms.CharField(
        label='Адрес доставки',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'})
    )
    text = forms.CharField(
        label='Комментарий к заказу',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите комментарий (необязательно)', 'rows': 3})
    )