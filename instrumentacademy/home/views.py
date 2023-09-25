from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField  # Import the reCAPTCHA field
from captcha.widgets import ReCaptchaV3
from django.conf import settings
from django.contrib.auth import authenticate,login as userlogin, logout

from hashlib import sha256
from .models import *
from .forms import *
from django.core.paginator import Paginator


def index(request):
    course = category.objects.all()
    return render(request,'index.html',{'course': course})

def index(request):
    categories = category.objects.all()  
    paginator = Paginator(categories, 6)  # Show 10 categories per page (adjust as needed)
    page_number = request.GET.get('page')  # Get the current page number from the request

    categories = paginator.get_page(page_number) 
    context = {'categories': categories}  
    
    return render(request, 'index.html', context)


def loggout(request):
    logout(request)
    return render(request,'login.html')

def base(request):
    return render(request,"base.html" )

def forget(request):
    return render(request,"forget.html" )

def adminpage(request):
    return render(request,"webadmin/index.html" )

def homecontent(request):
    return render(request,"student_template/home_content.html" )

def index1(request):
    return render(request,"main_app/index1.html" )
def mylearning(request):
    return render(request,"My_learning.html" )

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        isT = request.POST.get('isTutor') == 'on'

        # Check if a file was uploaded for the resume
        resume = None
        if isT:
            resume = request.FILES.get('resume')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exists")
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.success(request, "Email already exists")
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user_profile = UserProfile.objects.create(user=user, isTutor=isT, resume=resume)
                user.save()
                messages.success(request, "Registration success!!")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            messages.success(request, "Registration failed")
            return redirect('registration')
    return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_superuser:
                up = UserProfile.objects.get(user=user)
                
                if up.isTutor == 1:
                    # Tutor approval is pending
                    return render(request, 'login.html', {'error': "Pending admin approval"})

                elif up.isTutor == 2:
                    # Tutor is approved, redirect to tutor dashboard
                    userlogin(request, user)
                    request.session['username'] = username
                    return redirect('view_profile_tutor')  # Use the actual URL name

                else:
                    # Redirect learners to the learner dashboard
                    userlogin(request, user)
                    request.session['username'] = username
                    return redirect('index')  # Use the actual URL name

            elif user.is_superuser:
                userlogin(request, user)
                return redirect('admin_dashboard/home/')  # Use the actual URL name

        else:
            messages.error(request, "Invalid Username/Password")

    return render(request, 'login.html')


def student_view_result(request):

    return render(request, "student_template/student_view_result.html")

def logout_user(request):
   
    return render(request, "student_template/student_view_result.html")
def user_logout(request):
   
    return render(request, "student_template/student_view_result.html")

def student_fcmtoken(request):
    return render(request, "student_template/student_view_result.html")


def course_material(request):
    return render(request,"tutor_template/course_material.html" )

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to your desired page after login
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')