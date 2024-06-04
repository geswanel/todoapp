from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import RegisterForm


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. "
                             "You are able to log in now.")
            return redirect(reverse('users:login'))
    return render(request, 'users/register.html', {'form': form})
