from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def landing(request):
    if request.user.is_authenticated:
        return redirect("/tasks/")
    return render(request, "landing.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/tasks/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def custom_404(request, exception):
    return render(request, "404.html", status=404)