from django.shortcuts import redirect, render, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.forms import UserLoginForm, UserRegistrationForm
from tasks.models import Team, UserTeam
from subscriptions.models import PremiumUser


def is_premium(user):
    try:
        return user.premiumuser
    except PremiumUser.DoesNotExist:
        return False
    except AttributeError:
        return False


def index(request):
    """Return landing page"""
    is_premium_user = is_premium(request.user)

    if is_premium_user:
        return redirect(reverse('tasks_table'))
    elif request.user.is_authenticated:
        # User registerd but not premium
        return redirect(reverse('subscribe'))
    else:
        # Unknown user
        return render(request, 'accounts/index.html')


def logout(request):
    """Logout user"""
    auth.logout(request)
    messages.success(request, 'Logged out.  See you soon!')
    return redirect(reverse('index'))


def login(request):
    """Return Login Page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(
                request=request,
                username=request.POST['username_or_email'],
                password=request.POST['password']
            )
            if user:
                auth.login(user=user, request=request)
                messages.success(
                    request, f'Logged in.  Welcome { user.username.title() }!')
                return redirect(reverse(('index')))
            else:
                login_form.add_error(None, 'Incorrect login details')
    else:
        login_form = UserLoginForm()

    return render(request, 'accounts/login.html', {'login_form': login_form})


def registration(request):
    """Render the registration page"""

    if request.user.is_authenticated:
        return redirect(reverse(('index')))

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(
                request=request,
                username=request.POST['username'],
                password=request.POST['password1']
            )
            if user:
                auth.login(user=user, request=request)

                # Add user to default UserTeam
                default_team = Team.objects.get(pk=1)
                user_team = UserTeam.objects.create(ut_user=user, ut_team=default_team)
                user_team.save()

                messages.success(request, 'You are registered!')
                messages.success(
                    request, f'Welcome to Tasking  { user.username.title() }!')
                return redirect(reverse('index'))
            else:
                messages.error(
                    request, 'Unable to register at this time. Please try again')
    else:
        registration_form = UserRegistrationForm()

    return render(request, 'accounts/registration.html',
                  {'registration_form': registration_form})

# TODO
@login_required
def user_profile(request):
    """User's profile Page"""

    user = User.objects.get(email=request.user.email)
    return render(request, 'accounts/profile.html', {'profile': user})
