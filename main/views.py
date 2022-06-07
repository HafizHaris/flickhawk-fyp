from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render,HttpResponse
from notifications.signals import notify



def home(request):
    return render(request,'main/home.html')

def aboutus(request):
    return render(request,'main/aboutus.html')

def terms(request):
    return render(request,'main/terms.html')

def contactus(request):
    return render(request,'main/contactus.html')

def tools(request):
    return render(request,'main/tools.html')

def notfound(request):
    return render(request,'main/404.html')

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = None
        try:
            user = User.objects.get(email=email.lower())
        except:
            messages.error(request, "Email does not exist")
        
        if user is not None:
            # username = get_user(email)
            user = authenticate(request,username=user,password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request, "Username OR password is incorrect")

    page = 'login'
    context = {'page':page}
    return render(request,'main/login_register.html',context)   

def logoutUser(request):
    logout(request)
    # messages.error(request, "User was logged out!")
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email= request.POST['email']
            if not User.objects.filter(email=email.lower()).count() > 0:
                user = form.save(commit=False) 
                user.username = user.username.lower()
                user.save()
                login(request, user)
                notify.send(user, recipient=user, verb='Welcome to the FlickHawk.')
                return redirect('dashboard')
            else:
                messages.error(request, "This email is already registered!")
        else:
            messages.error(request, "An error has occured during registration!")


    context = {'page':page,'form':form}
    return render(request, 'main/login_register.html',context)