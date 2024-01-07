from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                msg = "User created - please <a href='/login'>login</a>."
                success = True
                # return redirect("/login/")
            else:
                msg = "User creation failed"
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "cadastro/register.html", {"form": form, "msg": msg, "success": success})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "cadastro/login.html", {"form": form, "msg": msg})
