from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import login_form, signup_form
from .models import User, Profile
def signup(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': signup_form(), 
                                                       'message': 'form is not valid'})
            
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=name).first():
            return render(request, 'signup.html', {'form': signup_form(), 
                                                    'message': 'username already exists'})
        new_user = User(username=name, email=email, password=password)
        new_user.save()
        request.session['logged'] = name
    return render(request, 'signup.html', {'form': signup_form()})

def login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if not form.is_valid():
            return render(request, 'login.html', {'form': login_form(), 
                                                  'message': 'form is not valid'})
        name = request.POST.get('name')
        password = request.POST.get('password')
        attempted_user =  User.objects.filter(username=name).first()
        if not attempted_user:    
            return render(request, 'login.html', {'form': login_form(), 
                                                  'message': 'user does not exist'})
        if password == attempted_user.password:
            request.session['logged'] = attempted_user.username
            return redirect(reverse('home page'))
        else:
            return render(request, 'login.html', {'form': login_form(), 
                                                  'message': 'wrong username or password'})
       
    return render(request, 'login.html', {'form': login_form()})


def logout(request):
    request.session['logged'] = False
    return render(request, 'logout.html')

def homepage(request):
    return redirect(reverse('home page'))
    

def profilepage(request, user):
    if request.session.get('logged', None):
        profile = Profile.objects.filter(username=user)
        if profile:
            profile_posts = profile.posts
        return render(request, 'profilepage.html', {'profile_posts': profile_posts})
    else:
        return redirect(reverse('log in'))
