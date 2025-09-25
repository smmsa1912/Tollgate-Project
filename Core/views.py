from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm


# Create your views here.


class HomeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        return render(request, 'home.html')


class LoginView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        data = {
            'form': LoginForm()
        }
        return render(request, 'login.html', data)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, Email=form.cleaned_data["Email"], password=form.cleaned_data["Password"])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                data = {
                    'form': form,
                    'error': 'Invalid Email or Password'
                }
                return render(request, 'login.html', data)
        else:
            data = {
                'form': form
            }
            print(form.errors)
            return render(request, 'login.html', data)


class RegisterView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'register.html', data)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            data = {
                'form': form
            }
            print(form.errors)
            return render(request, 'register.html', data)


def Logout(request):
    logout(request)
    return redirect("login")
