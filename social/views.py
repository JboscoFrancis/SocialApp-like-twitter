from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from . forms import PostForm, CommentForm, UpdateProfile, UpdateProfilePic
from django.db import IntegrityError
from . models import *
from django.http import JsonResponse
import json


# Create your views here.
def home(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if request.user.is_authenticated:
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                messages.info(request, f'post posted')
                return redirect('home')
            else:
                messages.error(request, f'post not sent')
        else:
            messages.info(request, f'Sorry your not logged in')

    post = Post.objects.all().order_by('-date_added')
    paginator = Paginator(post, 5)     #post pagination
    page_num = request.GET.get('page')
    post = paginator.get_page(page_num)

    context = {'post':post, 'form':form}
    return render(request, 'social/home.html', context)

def register(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm-password']

        if password!=confirmpassword:
            messages.warning(request, f'password dint match')
        else:
            #create user
            try:
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                # create user profile picture
                user_pic = Profile.objects.create(
                    user = user
                )
                user.save()
                user_pic.save()
                #add user to follower
                user_follower = Follower(user=user)
                user_follower.save()

                #login user after registered
                login(request,user)
                messages.success(request, f'account for ' + username + ' created successfully')
                return redirect('home')
            except IntegrityError:
                messages.warning(request, f'username already exist')
                return redirect('register')
    return render(request, 'social/register.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'you have logged in successfully')
            return redirect('home')
        else:
            messages.warning(request, f'invalid username or password')
    return render(request, 'social/user_login.html')

def userlogout(request):
    logout(request)
    return redirect('home')

def user_profile(request, pk):
    # Get user
    profile = User.objects.get(id=pk)
    try:
        follow = Follower.objects.get(user=profile)
        following = follow.follower.count() # Get all who following
        followers = User.objects.filter(follower__follower=profile).count() # Get all followers
    except Follower.DoesNotExist:
        follow = 0
        following = 0
        followers = 0
    # Get Posts from user
    post = Post.objects.filter(user=profile).order_by('-date_added').all()
    context = {'post':post, 'following':following, 'followers':followers, 'profile':profile, 'follow':follow}

    return render(request, 'social/user_profile.html', context)
    
@login_required(login_url='userlogin')
def update_profile(request, pk):
    user = User.objects.get(id=pk)
    u_form = UpdateProfile(instance=user)
    p_form = UpdateProfilePic(instance=user)
    if request.method == 'POST':
        u_form =UpdateProfile(request.POST, instance=request.user)
        p_form =UpdateProfilePic(request.POST,request.FILES, instance=request.user.profile)
        if u_form and p_form.is_valid():
            p_form.instance.user = user
            u_form.save()
            p_form.save()
            messages.success(request, f'Updated successfully')
            return redirect('user_profile', pk)
        else:
            messages.warning(request, f'something went wrong')
    context = {'user':user, 'u_form':u_form, 'p_form':p_form}
    return render(request, 'social/update_profile.html', context)

@login_required(login_url='userlogin')
def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user.id == post.user.id:
            form =PostForm(instance=Post.objects.get(id=pk))
            if request.method == 'POST':
                form = PostForm(request.POST, instance=post)
                #Get post user
                postuser = post.user
                form.instance.user = postuser
                if form.is_valid():
                    form.save()
                    messages.info(request, f'Post edited successfully')
                    return redirect('post_detail', pk)
                else:
                    messages.error(request, f'there was an error during sending post, plz correct fields')
            context = {'form':form}
        else:
            messages.warning(request, f'you cant edit this post, not owner')
            return redirect('post_detail', pk)
    else:
        messages.error(request, f'not logged in')
    return render(request, 'social/edit_post.html', context)

def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    #Get other post from user
    userpost = Post.objects.filter(user=post.user).order_by('-date_added').exclude(id=pk)
    cform = CommentForm()
    if request.method == 'POST':
        cform = CommentForm(request.POST)
        cform.instance.user = request.user
        cform.instance.post = post
        if cform.is_valid:
            cform.save()
            return redirect('post_detail', pk)
    #get comment from that post
    try:
        comment = Comment.objects.filter(post=post).order_by('-date_added')
    except Comment.DoesNotExist:
        comment = []
    
    context = {'post':post, 'userpost':userpost, 'cform':cform, 'comment':comment}
    return render(request, 'social/post_detail.html', context)

@login_required(login_url='userlogin')
def delete_confirm(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, 'social/delete_confirm.html', context)

@login_required(login_url='userlogin')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.id == post.user.id:
        post.delete()
        messages.info(request, f'Post deleted successfully')
    else:
        messages.warning(request, f'your not owner of the post, you cant delete it')
    return redirect('home')


@csrf_exempt
def likePost(request):
    data = json.loads(request.body)
    postid = data['postId']
    action = data['action']
    post = Post.objects.get(id=postid)
    if request.user.is_authenticated:
        user = request.user
        if action == 'like':
            post.likes.add(user)
            post.save()
        elif action == 'unlike':
            post.likes.remove(user)
    else:
        messages.warning(request, f'Your not logged in')
    return JsonResponse('data sent', safe=False)

@csrf_exempt
def follow_user(request):
    data = json.loads(request.body)
    userId = data['userId']
    action = data['action']
    follower = Follower.objects.get(user=userId)
    if request.user.is_authenticated:
        user = request.user
        if action == 'follow':
            follower.follower.add(user)
            follower.save()
        elif action == 'unfollow':
            follower.follower.remove(user)
    else:
        messages.warning(request, f'Your not logged in')
    return JsonResponse('data sent', safe=False)
    