from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import User, Post

class NewPostForm(forms.Form):
    new_post = forms.CharField(label="", widget=forms.Textarea(attrs={'class': "post"}))

def index(request):
    
    # Check if method is POST
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as form
        form = NewPostForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            new_post = form.cleaned_data["new_post"]
            user = request.user

            # Attempt to create new user
            try:
                post = Post.objects.create(post=new_post, user=user)
            except IntegrityError:
                return render(request, "network/index.html", {
                    "message": "Post already exists."
                })            
                      
            return render(request, "network/index.html", {
                'form': NewPostForm(),
                'posts': Post.objects.all()
            })
        # If the form is invalid, re-render the page with existing information.    
        else:
            return render(request, "network/index.html", {
                'form': form
            })
    
    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'posts': Post.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
