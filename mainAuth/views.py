from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import AuthBackend, User
from .forms import UserRegistrationForm


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = AuthBackend()
        user = auth_backend.authenticate(request=request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
        return redirect('feed')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form': login_form})


def user_logout(request):
    logout(request)
    return redirect('feed')


@login_required
def user_subscribe(request, pk):
    try:
        subscribing = User.objects.get(pk=pk)
    except:
        return HttpResponseNotFound("404")

    if (subscribing not in request.user.subscriptions.all()) and (subscribing != request.user):
        request.user.subscriptions.add(subscribing)
        request.user.save()
        return redirect('feed')
    elif subscribing == request.user:
        return HttpResponseBadRequest("It's not allowed to subscribe itself")
    else:
        return HttpResponseBadRequest("user is already subscribed")
