# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse

from channel.models import Messages


@login_required(login_url='/log_in/')
def user_list(request):
    """
        Цей код можна використовувати лише для тесту, але не на продакшені.
        Уявіть як просяде продуктивність при 100 000 користувачів.
    """
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    messages = Messages.objects.select_related('user').order_by('-created_at')[:30]
    return render(request, 'example/user_list.html', {
        'users': users,
        'me': request.user,
        'messages': reversed(messages)
    })


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('channel:user_list'))
        else:
            print(form.errors)
    return render(request, 'example/log_in.html', {'form': form})


@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('channel:log_in'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('channel:user_list'))
        else:
            print(form.errors)
    return render(request, 'example/sign_up.html', {'form': form})

