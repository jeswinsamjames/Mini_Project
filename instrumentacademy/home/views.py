from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField  # Import the reCAPTCHA field
from captcha.widgets import ReCaptchaV3
from django.conf import settings
from django.contrib.auth import authenticate,login as userlogin, logout

from hashlib import sha256
from .models import *
from .forms import EditProfileForm


def index(request):
    return render(request,'index.html')

def blog(request):
    return render(request,'blog.html')
def sample(request):
    return render(request,"sample-inner-page.html")


def loggout(request):
    logout(request)
    return render(request,'login.html')

def base(request):
    return render(request,"base.html" )

def userdashboard(request):
    return render(request,"usersprofile.html" )


def courses(request):
    # Retrieve the course object using the course_id
    course = Course.objects.all()

    # Render a template to display the course details
    return render(request, 'courses.html', {'course': course})


def leanerindex(request):
    
    return render(request,"learner_index.html" )

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

# import requests
# from django.http import JsonResponse

# def verify_recaptcha(request):
#     if request.method == 'POST':
#         recaptcha_response = request.POST.get('token')
#         secret_key = 'YOUR_RECAPTCHA_SECRET_KEY'  # Replace with your reCAPTCHA secret key

#         # Send a request to Google to verify the reCAPTCHA token
#         response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
#             'secret': secret_key,
#             'response': recaptcha_response
#         })

#         result = response.json()

#         # Check if reCAPTCHA verification succeeded
#         if result['success']:
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False})









def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        isT = request.POST.get('isTutor') == 'on' 
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username alredy exist")
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.success(request, "Email alredy exist")
                return redirect('registration')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user_profile = UserProfile.objects.create(user=user, isTutor=isT)
                user.save();
            print("User Created");
            messages.success(request,"Registration success!!")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            messages.success(request,"Registration failed")
            return redirect('registration')
    return render(request, 'registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if not user.is_superuser:
            up = UserProfile.objects.get(user=user)

            if up.isTutor == 1:
                # Tutor approval is pending
                return render(request, 'login.html', {'error': "Pending admin approval"})

            elif up.isTutor == 2:
                # Tutor is approved, redirect to tutor dashboard
                userlogin(request, user)
                request.session['username'] = username
                return redirect('view_profile_tutor')  # Replace 'tutorindex' with the actual URL for the tutor dashboard
             
            # Redirect learners to the learner dashboard
            userlogin(request, user)
            request.session['username'] = username
            return redirect('learnerindex')  # Replace 'learnerindex' with the actual URL for the learner dashboard

        elif user.is_superuser:
            userlogin(request, user)    
            return redirect('admin_dashboard/home/')   
        else:
            messages.error(request, "Invalid Username/Password")
            return redirect('login')

    return render(request, 'login.html')


# def view_profile(request):
#     user = request.user
#     user_profile = user.userprofile  # Assuming the related name is 'userprofile'
    
#     context = {
#         'user_profile': user_profile,
#     }
    
#     return render(request, 'profile.html', context)

# def edit_profile_tutor(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             user = form.save(commit=False)

#             # Access the UserProfile object associated with the User
#             user_profile = UserProfile.objects.get(user=user)

#             # Update gender, address, first name, and last name
#             user_profile.gender = request.POST['gender']
#             user_profile.address = request.POST['address']
#             user.last_name = request.POST['last_name']
#             user.first_name = request.POST['first_name']
            
#             user_profile.save()  # Save the UserProfile
#             user.save()  # Save the User

#             return redirect('profile')
#     else:
#         form = EditProfileForm(instance=request.user)

#     context = {
#         'form': form,
#     }

#     return render(request, 'student_template/profile.html', context)

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def tutorslist(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutorslist.html', {'tutors': tutors})


def tutorslist_2(request,instrument=None):
    tutors = Tutor.objects.filter(instrument_teaching__icontains=instrument)
    return render(request, 'tutorslist.html', {'tutors': tutors})









def student_view_result(request):
    # student = get_object_or_404(Student, admin=request.user)
    # results = StudentResult.objects.filter(student=student)
    # context = {
    #     'results': results,
    #     'page_title': "View Results"
    # }
    return render(request, "student_template/student_view_result.html")

def logout_user(request):
   
    return render(request, "student_template/student_view_result.html")
def user_logout(request):
   
    return render(request, "student_template/student_view_result.html")

def student_fcmtoken(request):
    return render(request, "student_template/student_view_result.html")



# <<<<<<<<<<<admin viewss>>>>>>>>>>>>>>>


def webadmin(request):
    # postcount = Post.objects.all().count()
    # catcount = Category.objects.all().count()
    # usercount = User.objects.all().count()
    # orders = Order.objects.all()
    # context = {'postcount':postcount, 'cat':catcount, 'user':usercount,"orders":orders}
    return render(request, 'webadmin/index.html')  
def allposts(request):
    # posts = Post.objects.all()
    # context = {'posts':posts}
    return render(request, 'webadmin/allposts.html')
def allcat(request):
    # cat = Category.objects.filter(parent=None).order_by('hit')
    # context = {'cat':cat}
    return render(request, 'webadmin/allcat.html')
def allusers(request):
    # users = User.objects.all()
    # customer = Customer.objects.all()
    # context = {
    #     # 'users':users
    # 'customer':customer
    # }
    return render(request, 'webadmin/allusers.html')
def allorders(request):
    # orders = Order.objects.filter(ordered=True)
    # carts = Cart.objects.all()
    # context = {
    # 'orders':orders, 'carts':carts,
    # }
    return render(request, 'webadmin/allorders.html')

from .models import *
from .forms import *    
def allvideos(request):
    vid = video.objects.all()
    context = {'video':vid}
    return render(request, 'webadmin/allvideo.html', context)


