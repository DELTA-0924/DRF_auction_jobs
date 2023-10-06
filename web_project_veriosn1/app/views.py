"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest,JsonResponse
from .models import CustomUser;
from .forms import CustomUserCreationForm,CustomLoginForm 
from django.contrib import messages

def home(request):    
    is_authenticated = request.user.is_authenticated
    users=CustomUser.objects.all();
    context = {
              'is_authenticated': is_authenticated,
              'users':users
        }
    if request.user.is_authenticated:
        # Если пользователь аутентифицирован, вы можете получить его данные
        user = request.user
        # Теперь у вас есть доступ к данным пользователя
        username = user.fio
        usernickname=user.username
        # и так далее...
        # Добавьте эти данные в контекст и передайте их в шаблон
        context = {
            'username': username,
            'usernickname': usernickname,           
            'is_authenticated': is_authenticated,
            'users':users
        }
    user_data = [{'name': user.username} for user in users]    
    assert isinstance(request, HttpRequest)
    return JsonResponse({'users': user_data}, safe=False)
    # return render(
    #     request,
    #     'app/index.html',context
    # )
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Добавьте логику для обработки успешной регистрации, например, отправку email-подтверждения или перенаправление на другую страницу.
            return redirect('home')  # Замените 'success_page' на имя вашей страницы успешной регистрации.
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Добавьте логику после успешной авторизации, например, перенаправление на другую страницу.
                return redirect('home')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль.')
    else:
        form = CustomLoginForm(request)

    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')