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


def google_logout(request):
    # Revoke the access token from Google
    if 'access_token' in request.session:
        access_token = request.session['access_token']
        # Implement the code to revoke the access token from Google using the API
        # For example, using the requests library:
        # import requests
        # revoke_url = f"https://accounts.google.com/o/oauth2/revoke?token={access_token}"
        # response = requests.get(revoke_url)
        # if response.status_code == 200:
        #     del request.session['access_token']
        # else:
        #     print("Failed to revoke access token")
        del request.session['access_token']  # Remove the token from session

    # Clear user session data
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('/login') 

def forget(request):
    return render(request,"forget.html" )
