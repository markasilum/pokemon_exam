from django.forms import ModelForm
from django.contrib.auth.models import User
from pokemons.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login


class UserRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'register.html', {'form': form})