from django import forms
from .models import CustomUser
from .signin import EmailAuthBackend
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторіть введення пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('firstname', 'lastname', 'email', 'age', )
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
        }
        labels = {
            'firstname': "Ім'я",
            'lastname': "Прізвище",
            'email': 'Електронна пошта',
            'age': 'Вік'
        }


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label='Електронна поштa', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            self.user_cache = EmailAuthBackend().authenticate(email=email, password=password)

    def get_user(self):
        return self.user_cache