from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField  # Import the reCAPTCHA field
from captcha.widgets import ReCaptchaV3
from django.conf import settings
from django.contrib.auth import authenticate,login as userlogin, logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from hashlib import sha256
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

def get_recommended_courses(courses):
    recommended_courses = sorted(courses, key=lambda x: x.sentiment_score if x.sentiment_score is not None else 0, reverse=True)[:5]
    return recommended_courses
def map_sentiment_to_star_rating(sentiment_score):
    if sentiment_score is None:
        return None
    rating = round((float(sentiment_score) + 1) * 2.5, 1)  # Convert Decimal to float and then perform arithmetic
    return rating


def index(request):
    query = request.GET.get('q')
    
    # Fetch all courses
    courses = CourseDetail.objects.all()
    
    # Integrate sentiment analysis recommendation logic
    recommended_courses = get_recommended_courses(courses)
    
    # Fetch categories for pagination
    categories = category.objects.all()
    paginator = Paginator(categories, 6)  # Show 6 categories per page
    
    # Get page number from request
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    # Count wishlist items if user is authenticated
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    
    # Prepare average rating data for each course
    average_ratings = []
    for course in courses:
        sentiment_score = course.sentiment_score
        star_rating = map_sentiment_to_star_rating(sentiment_score)
        average_ratings.append((course, star_rating))
    
    # Sort courses in decreasing order of star ratings
    average_ratings = sorted(average_ratings, key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=True)
    
    context = {
        'courses': courses,
        'query': query,
        'recommended_courses': recommended_courses,
        'categories': categories,
        'wishlist_count': wishlist_count,
        'average_ratings': average_ratings,
    }
    
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')[:10]
        data = [{'content': notification.content, 'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M')} for notification in notifications]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@csrf_exempt
def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def search_results(request):
    query = request.GET.get('query')
    if query:
        results = CourseDetail.objects.filter(name__icontains=query)
        # You can customize this queryset based on your model and search criteria
        print(results)
        return render(request, 'tutor_template/search_results.html', {'results': results})
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)
    


def metronome(request):

    return render(request, "metronome.html")

def paino_keys(request):
    return render(request, "student_template/paino_keys.html")