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
            messages.info(request,"Invalid Credentials!")
    return render(request,"login.html")



def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        confirmpassword=request.POST.get('cnpass')
        if confirmpassword==password:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists!')
                return render(request,'register.html')
            else :
                user_reg=User.objects.create_user(username=username,email=email,password=password)
                user_reg.save()

            # Handle user registration here (create user, log in, etc.)
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')  # Redirect to login page
        else:
            messages.error(request,'Password does not match')
            return render(request,'reg.html')
    return render(request, 'register.html')

def base(request):
    return render(request,"base.html" )

def forget(request):
    return render(request,"forget.html" )
