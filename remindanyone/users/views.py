from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from users.forms import CustomUserCreationForm

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist!")
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Password incorrect!")
    return render(request, 'users/login.html')

def logout_user(request):
    # messages.success(request, "User was logged out.")
    logout(request)
    return redirect('login')

def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User created successfully!")

            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(
                request, 'An error has occured during registration!')

    context = {"form": form}
    return render(request, 'users/register.html', context)



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'users/dashboard.html')
