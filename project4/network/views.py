import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Profile
from .forms import NewPostForm

def index(request):
    # If user is logged in then show posts and new post page
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
                form = NewPostForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['new_post']
                    new_post = Post.objects.create(author=user_profile, content=content)
                    new_post.save()
                    return HttpResponseRedirect(reverse("index"))
        else:
            form = NewPostForm()

        paginator = Paginator(Post.objects.all().order_by('post_date').reverse(), 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, "network/posts.html", {"form": form, "page_obj": page_obj, "user_profile": user_profile})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def edit(request, post_id):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        form = NewPostForm({'new_post': data['new_content']})
        if not form.is_valid():
            return JsonResponse({
                "error": "Form is invalid"}, status=402)

        post = Post.objects.filter(author=user_profile).get(id=data['post_id'])
        if post is None:
            return JsonResponse({
                "error": "Post not found"
            }, status=400)
        
        new_content = form.cleaned_data['new_post']
        post.content = new_content
        post.save()
        return HttpResponse(status=204)
    
    # Email must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=401)



@login_required
def profile(request, profile_id):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':       
        data = json.loads(request.body)
        profile = Profile.objects.get(id=data['user_id'])
        btn_value = data['btn_value']
        if profile is not None:
            if btn_value == 'FOLLOW':
                user_profile.add_relationship(profile)
                user_profile.save()              
            if btn_value == 'UNFOLLOW':
                user_profile.delete_relationship(profile)
                user_profile.save()
            message = f'You {btn_value.lower()}ed {profile} successfully!'
            return JsonResponse({"status": 200, "message": message})

        else:
            return JsonResponse(status=404)
    # Get request
    else:
        profile = Profile.objects.get(id=profile_id)
        if profile is not None:
            profile_paginator = Paginator(Post.objects.filter(author=profile_id).order_by('post_date').reverse(), 10)
            page_number = request.GET.get('page', 1)
            page_obj = profile_paginator.get_page(page_number)
            return render(request, "network/profile.html", {"profile": profile, 
                                                            "page_obj": page_obj,
                                                            "user_profile": user_profile
                                                            })

@login_required
def following(request):
    user_profile = Profile.objects.get(user=request.user)
    following_posts = []
    # Getting all the Post objects from the users that the current user follows
    for user in list(user_profile.get_following()):
        following_posts.extend(Post.objects.filter(author=user).order_by('post_date').reverse())
    
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {"page_obj": page_obj, "user_profile": user_profile})

@login_required
def like(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(id=data['post_id'])
        if post is not None:
            liked = False
            if user_profile in post.likes.all():
                post.likes.remove(user_profile)
                liked = True
            else:
                post.likes.add(user_profile)
            return JsonResponse({'likes': post.get_total_likes(), "liked": liked})


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
            user_profile = Profile.objects.create(user=user)
            user_profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")