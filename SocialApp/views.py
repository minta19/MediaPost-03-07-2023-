from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserLoginForm,UserRegistrationForm,ProfilePictureForm,ProfileForm,CreatePostForm
from django.contrib.auth.forms import get_user_model
from django.contrib.auth import authenticate,login,logout
from .models import Post,Profile,FollowersCount
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request,'socialapp/home.html')

def userLogin(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print('Username:', username)
            print('Password:', password)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
           user= form.save()
           login(request,user)
           return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('home/')  

@login_required
def post_list(request):
    posts=Post.objects.filter(user=request.user)
    context={
        'posts':posts
    }
    return render(request,'socialapp/post_features.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('dashboard')  
    else:
        form = CreatePostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'socialapp/createpost.html', context)

@login_required
def delete_post(request,post_id):
    posts=get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        posts.delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')
    
@login_required
def edit_post(request,post_id):
    posts=get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        form=CreatePostForm(request.POST,instance=posts)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
            form=CreatePostForm(instance=posts)
    return render(request,'socialapp/postedit.html',{'form':form,'post_id':post_id})
    



