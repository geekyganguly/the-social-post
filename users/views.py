from .forms import RegisterForm, LoginForm, ChangePasswordForm, EditProfileForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = User.objects.get(phone=phone).username
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'Logged in.')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('index')
            else:
                messages.error(
                    request, "Account not found!.")
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        form = LoginForm()

    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'users/login.html', context=context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered. Login now')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        form = RegisterForm()

    context = {
        'title': 'Sign up',
        'form': form,
    }
    return render(request, 'users/register.html', context=context)


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect("index")


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Password Changed. Login back.')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong!! Please try again')

    else:
        form = ChangePasswordForm(user=request.user)

    context = {
        'title': 'Change Password',
        'form': form,
    }
    return render(request, 'users/change_pass.html', context=context)


def profile(request, username):
    user_profile = User.objects.get(username=username)
    profile_connections = [user for user in user_profile.connection.all()]

    if request.user.is_authenticated:
        my_connections = [user for user in request.user.connection.all()]
        mutual_connections = list(
            set(my_connections).intersection(set(profile_connections)))
    else:
        mutual_connections = None

    if request.user.is_authenticated and user_profile in request.user.connection.all():
        posts = user_profile.post_set.all().order_by('-updated_date')
    else:
        posts = user_profile.post_set.all().filter(
            is_public=True).order_by('-updated_date')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile', username=form.cleaned_data['email'].split('@')[0])
        else:
            messages.error(request, 'Something went wrong!! Please try again')
    else:
        form_data = {
            'name': user_profile.first_name + ' ' + user_profile.last_name,
            'bio': user_profile.bio,
            'phone': user_profile.phone,
            'email': user_profile.email,
            'profile_pic': user_profile.profile_pic,
        }
        form = EditProfileForm(user=request.user, initial=form_data)
    context = {
        'user_profile': user_profile,
        'posts': posts,
        'profile_connections': profile_connections,
        'mutual_connections': mutual_connections,
        'form': form,
    }
    return render(request, 'users/profile.html', context=context)


def search(request):
    if request.is_ajax():
        search = request.POST.get('search')
        qs = User.objects.filter(
            Q(username__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) | Q(first_name__icontains=search)).exclude(username=request.user)
        if len(qs) > 0 and len(search) > 0:
            data = []
            if request.user.is_authenticated:
                data1 = []
                data2 = []
                for i in qs:
                    if i in request.user.connection.all():
                        item = {
                            'username': i.username,
                            'name': i.get_full_name(),
                            'profile_pic': i.profile_pic.url,
                            'connection': i.connection.count(),
                            'is_authenticated': True,
                            'is_connected': True,
                        }
                        data1.append(item)
                    else:
                        item = {
                            'username': i.username,
                            'name': i.get_full_name(),
                            'profile_pic': i.profile_pic.url,
                            'connection': i.connection.count(),
                            'is_authenticated': True,
                            'is_connected': False,
                        }
                        data2.append(item)
                data = data1 + data2
            else:
                for i in qs:
                    item = {
                        'username': i.username,
                        'name': i.get_full_name(),
                        'profile_pic': i.profile_pic.url,
                        'connection': i.connection.count(),
                        'is_authenticated': False,
                        'is_connected': False,
                    }
                    data.append(item)
            result = data
        else:
            result = 'User not found......'
        return JsonResponse({'data': result})
    return JsonResponse({})


@login_required
def connect_user(request):
    if request.is_ajax():
        id = request.GET.get('id')
        user_to_connect = User.objects.get(id=id)
        updated = False
        connected = False
        if request.user in user_to_connect.connection.all():
            user_to_connect.connection.remove(request.user)
            connected = False
        else:
            user_to_connect.connection.add(request.user)
            connected = True
        updated = True
        total_connections = user_to_connect.connection.count()
        data = {
            'updated': updated,
            'connected': connected,
            'total_connections': total_connections,
        }
        return JsonResponse({'data': data})
    return JsonResponse({})
