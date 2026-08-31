from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Ім'я", max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Зрозуміла помилка при спробі повторної реєстрації
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email вже зареєстрований.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")