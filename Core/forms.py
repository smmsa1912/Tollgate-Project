from django import forms
from django.core.exceptions import ValidationError

from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['First_Name', 'Last_Name', 'Phone_Number', 'Email', 'password1', 'password2']
        First_Name = forms.CharField(max_length=50, widget=forms.TextInput)
        Last_Name = forms.CharField(max_length=50, required=False, widget=forms.TextInput)
        Phone_Number = forms.CharField(max_length=10, widget=forms.NumberInput)
        Email = forms.EmailField(widget=forms.EmailInput)
        password1 = forms.CharField(max_length=50, widget=forms.PasswordInput, min_length=8)
        password2 = forms.CharField(max_length=50, widget=forms.PasswordInput, min_length=8)

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_Email(self):
        Email = self.cleaned_data.get("Email")
        if User.objects.filter(Email=Email).exists():
            raise forms.ValidationError("Email already exists")
        return Email

    def clean_First_Name(self):
        Name = self.cleaned_data.get("First_Name")
        if len(Name) < 2:
            raise forms.ValidationError("Name must be at least 3 characters")
        return Name

    def clean_Last_Name(self):
        Name = self.cleaned_data.get("Last_Name")
        if Name:  # last name is optinal
            if len(Name) < 2:
                raise forms.ValidationError("Name must be at least 3 characters")

        return Name

    def clean_Phone_Number(self):
        Phone_Number = self.cleaned_data.get("Phone_Number")
        if len(Phone_Number) != 10:
            raise forms.ValidationError("Phone number must be 10 characters only")
        if not Phone_Number.isdigit():
            raise forms.ValidationError("Phone number must be only digits")
        if User.objects.filter(Phone_Number=Phone_Number).exists():
            raise forms.ValidationError("Phone number already exists")
        return Phone_Number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    Email = forms.EmailField(widget=forms.EmailInput, required=True)
    Password = forms.CharField(max_length=50, widget=forms.PasswordInput, min_length=8)

    def clean_Email(self):
        Email = self.cleaned_data.get("Email")
        if not User.objects.filter(Email=Email).exists():
            raise forms.ValidationError("Email does not exist")
        return Email

    def clean_Password(self):
        Email = self.cleaned_data.get("Email")
        Password = self.cleaned_data.get("Password")
        if len(Password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        try:
            user = User.objects.get(Email=Email)
        except User.DoesNotExist:
            raise forms.ValidationError("User Not Found")
        if not user.check_password(Password):
            raise forms.ValidationError("Password is incorrect")
        return Password
