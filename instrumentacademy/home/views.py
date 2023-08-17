from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User,auth
from captcha.fields import ReCaptchaField  # Import the reCAPTCHA field
from captcha.widgets import ReCaptchaV3
from django.conf import settings

def index(request):
    return render(request,'index.html')

def blog(request):
    return render(request,'blog.html')
def sample(request):
    return render(request,"sample-inner-page.html")
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # if recaptcha_response:
        #     response = captcha_verify(recaptcha_response)
        #     if not response['success']:
        #         messages.error(request, 'reCAPTCHA verification failed. Please try again.')
        #         return render(request, 'login.html')
            
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else :
            messages.error(request,"Invalid Credentials!")
            return redirect('/login')
    return render(request,"login.html")



def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirmpassword = request.POST.get('cnpass')

        if password != confirmpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('/register')
        
        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Username already taken.')
            return redirect('/register')
        except User.DoesNotExist:
            pass
        
        try:
            user = User.objects.get(email=email)
            messages.warning(request, 'Email id already exists.')
            return redirect('/register')
        except User.DoesNotExist:
            pass
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('/login')
        
    return render(request, 'register.html')

def base(request):
    return render(request,"base.html" )

def forget(request):
    return render(request,"forget.html" )
