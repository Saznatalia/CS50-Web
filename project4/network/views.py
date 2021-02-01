from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import User, Post

class NewPostForm(forms.Form):
    new_post = forms.CharField(label="", widget=forms.Textarea(attrs={'class': "post"}))

def index(request, *args, **kwargs):
    print(args, kwargs)
    
    # Check if method is POST
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as form
        form = NewPostForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            new_post = form.cleaned_data["new_post"]
            user = request.user

            # Attempt to create new post
            try:
                post = Post.objects.create(user=user, content=new_post)
            except:
                return render(request, "network/index.html", {
                    "message": "Post already exists."
                })            
                      
            return render(request, "network/index.html", {
                'form': NewPostForm(),
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

def post_detail(request, post_id, *args, **kwargs):
    
    data = {
        "id": post_id,    
    }
    status = 200
    try:
        post = Post.objects.get(id=post_id)
        data['content'] = post.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)

def posts(request, *args, **kwargs):
    return render(request, "network/posts.html")

def api_posts(request, *args, **kwargs):
    all_posts = Post.objects.all()
    data_list = [{"id": x.id, "content": x.content} for x in all_posts]
    data = {
        "response": data_list
    }
    return JsonResponse(data)

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
