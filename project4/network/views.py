import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
                # data = json.loads(request.body)
                form = NewPostForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data['new_post']
                    new_post = Post.objects.create(author=profile, content=content)
                    new_post.save()
                    return HttpResponseRedirect(reverse("index"))
        else:
            form = NewPostForm()

        paginator = Paginator(Post.objects.all().order_by('post_date').reverse(), 10)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        # posts = [x.serialize() for x in page_obj]
        return render(request, "network/posts.html", {"form": form, "page_obj": page_obj})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def post_detail(request, post_id, *args, **kwargs):  
    data = {
        "id": post_id,    
    }
    status = 200
    try:
        post = Post.objects.get(id=post_id)
    except Exception as ex:
        print(ex)
        data['message'] = "Not found"
        status = 404
    return JsonResponse(post.serialize(), status=status)


@login_required
def profile(request, profile_id):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':       
        data = json.loads(request.body)
        profile = Profile.objects.get(id=data['user_id'])
        btn_value = data['btn_value']
        if profile is not None:
            if btn_value == 'FOLLOW':
                print(str(user_profile.user.username) + " wants to follow " + str(profile.user.username))
                user_profile.add_relationship(profile)
                return JsonResponse(status=201, message="Successfully followed!")
                
            if btn_value == 'UNFOLLOW':
                print(str(user_profile.user.username) + " wants to unfollow " + str(profile.user.username))
                user_profile.delete_relationship(profile)
                return JsonResponse(status=202, message="Successfully unfollowed!")
                
        else:
            return JsonResponse(status=404)

    # Info about profile to display
    profile = Profile.objects.get(id=profile_id)
    if profile is not None:
        profile_n_followers = len(profile.get_followers())
        profile_n_following = len(profile.get_following())
        profile_paginator = Paginator(Post.objects.filter(author=profile_id).order_by('post_date').reverse(), 10)
        page_number = request.GET.get('page', 1)
        page_obj = profile_paginator.get_page(page_number)
        return render(request, "network/profile.html", {"username": profile.user.username, 
                                                        "profile_id": profile_id,
                                                        "profile": profile, 
                                                        "page_obj": page_obj,
                                                        "n_followers": profile_n_followers,
                                                        "n_following": profile_n_following,
                                                        "user_following_list": user_profile.get_following()
                                                        })

@login_required
def following(request):
    # If user is logged in then show posts and new post page
    if request.user.is_authenticated:
        # List of all user objects that the request user(current user) follows
        following_list = []
        user=request.user
        print(user)
        # Queryset of Profile class of user following
        following_list_query = user.following.all()
        print(user.follower.all)
        print(following_list_query)
        # Extracting the user object from the Profle queryset of user following
        for following in following_list_query:
            following_list.append(following.following)
            print(following.following)
        print(following_list)

        posts = []
        # Getting all the Post objects from the users that the current user follows
        for user in following_list:
            posts.extend(Post.objects.filter(user=user).order_by('post_date').reverse())
        
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/following.html", {"page_obj": page_obj})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


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
