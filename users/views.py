import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.http import JsonResponse
from .models import Profile
from copy import deepcopy


def login_user(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.warning(request, 'Username or password is incorrect.')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('posts:feed')
            messages.warning(request, 'Username or password is incorrect.')

    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'You have been logged out.')
    return redirect('posts:feed')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created.')

            return redirect('users:edit_profile')

        errors = '\n'.join([error for field_errors in form.errors.values() for error in field_errors])
        messages.warning(request, errors)

    context = {
        'form': form,
    }

    return render(request, 'users/registration.html', context)


@login_required(login_url='users:login')
def edit_profile(request):
    profile = request.user.profile
    profile_copy = deepcopy(profile)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.has_changed():
                if 'display_name' in form.changed_data and not form.cleaned_data.get('display_name'):
                    profile.display_name = form.cleaned_data['username']
                form.save()
                messages.success(request, 'Your profile has been updated.')
            return redirect('posts:feed')

        messages.warning(request, form.errors)

    context = {
        'form': form,
    }

    return render(request, 'users/profile_form.html', context)


def check_username(request):
    LOWER_LIMIT = 5
    UPPER_LIMIT = 17

    username = request.GET.get('username', None)

    if username:
        if not (LOWER_LIMIT <= len(username) <= UPPER_LIMIT):
            return JsonResponse({'available': False})

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return JsonResponse({'available': False})

        current_user = request.user if request.user.is_authenticated else None

        if Profile.objects.filter(username=username).exclude(user=current_user).exists():
            return JsonResponse({'available': False})

    return JsonResponse({'available': True})