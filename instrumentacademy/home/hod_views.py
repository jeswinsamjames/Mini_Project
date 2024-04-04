
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


from .forms import *
from .models import *

from django.db.models import Count
from collections import Counter
import json

def admin_home(request):
    # Count total students and tutors
    student_count = UserProfile.objects.filter(isTutor=0).count()
    tutor_count = UserProfile.objects.filter(isTutor=2).count()
    
    # Count total courses
    course_count = CourseDetail.objects.all().count()
    
    # Get attendance per course
    attendance_per_course = Attendance.objects.values('course__name').annotate(attendance_count=Count('id'))
    course_list = [item['course__name'] for item in attendance_per_course]
    attendance_list = [item['attendance_count'] for item in attendance_per_course]

    # Get attendance per student
    attendance_per_student = Attendance.objects.values('learner__username').annotate(attendance_count=Count('id'))
    student_list = [item['learner__username'] for item in attendance_per_student]
    student_attendance_list = [item['attendance_count'] for item in attendance_per_student]
    enrollment_data = Enrollment.objects.values('course__name').annotate(enrollment_count=Count('id'))

    course_list = [item['course__name'] for item in enrollment_data]
    enrollment_count_list = [item['enrollment_count'] for item in enrollment_data]

    specializations = UserProfile.objects.values_list('specialist', flat=True).exclude(specialist__isnull=True)
    specialization_counts = Counter(specializations)

    # Prepare data in a format suitable for the chart
    specialization_data = dict(specialization_counts)

    # Convert the data to JSON format
    specialization_data_json = json.dumps(specialization_data)


    context = {
        'student_count': student_count,
        'tutor_count': tutor_count,
        'course_count': course_count,
        'course_list': course_list,
        'attendance_list': attendance_list,
        'student_list': student_list,
        'student_attendance_list': student_attendance_list,
        'enrollment_count_list' : enrollment_count_list,
        'specialization_data_json': specialization_data_json
    }
    return render(request, 'hod_template/home_content.html', context)


def manage_staff(request):
    tutors = UserProfile.objects.filter(isTutor=2)
    context = {
        'all_tutors': tutors,
        'page_title': 'List of Tutors',  # You can set your page title here
    }
    return render(request, "hod_template/manage_staff.html", context)

def edit_tutor(request, tutor_id):
    tutor = get_object_or_404(UserProfile, id=tutor_id)  # Use UserProfile model here
    user = tutor.user  # Assuming user is the related user field in UserProfile model

    if request.method == 'POST':
        form = TutorForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            # Update tutor-specific fields
            tutor.gender = form.cleaned_data.get('gender')
            tutor.address = form.cleaned_data.get('address')
            tutor.specialist = form.cleaned_data.get('specialist')
            tutor.description = form.cleaned_data.get('description')
            tutor.phoneNo = form.cleaned_data.get('phoneNo')

            # Update the user fields
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            if password:
                user.set_password(password)

            # Handle profile picture
            profile_pic = request.FILES.get('profile_picture')
            if profile_pic:
                tutor.profile_picture = profile_pic

            user.save()
            tutor.save()
            messages.success(request, "Tutor profile updated successfully.")
            return redirect(reverse('edit_tutor', args=[tutor_id]))
        else:
            messages.error(request, "Please fill the form properly.")
    
    else:
        form = TutorForm(instance=user)
    
    context = {
        'form': form,
        'tutor_id': tutor_id,
        'page_title': 'Edit Tutor',
    }
    print(user)
    return render(request, "hod_template/edit_tutor_template.html", context)

def delete_tutor(request, tutor_id):
    user = get_object_or_404(User, id=tutor_id)
    if user.userprofile.isTutor == 2:
        user.delete()
        messages.success(request, "Tutor deleted successfully!")
    else:
        messages.error(request, "This user is not a tutor and cannot be deleted.")
    return redirect('manage_staff') 


class PendingTutorListView(ListView):
    model = UserProfile
    template_name = 'hod_template/pending_tutors.html'  # Create this template
    context_object_name = 'pending_tutors'
    
    def get_queryset(self):
        # Filter for pending tutors
        return UserProfile.objects.filter(isTutor=1)


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
@login_required
@staff_member_required
def approve_tutor(request, tutor_id):
    tutor = get_object_or_404(UserProfile, user__id=tutor_id, isTutor=1)

    # Approve the tutor by changing isTutor to 2
    tutor.isTutor = 2
    tutor.save()

    messages.success(request, "Tutor approved successfully!")

    return redirect('pending_tutors') 

def reject_and_delete_tutor(request, tutor_id):
    tutor = get_object_or_404(UserProfile, user__id=tutor_id, isTutor=1)

    # Reject the tutor by changing isTutor to 3 (or any other value that indicates rejection)
    tutor.isTutor = 3
    tutor.save()

    # Delete the tutor's user account
    user_id = tutor.user.id
    User.objects.get(id=user_id).delete()

    messages.success(request, "Tutor rejected and deleted successfully!")

    return redirect('pending_tutors')

def add_tutor(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username alredy exist")
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.success(request, "Email alredy exist")
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                tutor = UserProfile(user=user, isTutor=2)  # Automatically set isTutor to 2
                tutor.save()
                
                
            print("User Created");
            messages.success(request,"Registration success!!")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            messages.success(request,"Registration failed")
    return render(request, "hod_template/add_staff_template.html")


def manage_student(request):
    # Assuming you have a user_type field in your UserProfile model to distinguish students
    students = UserProfile.objects.filter(isTutor = 0)
    students = [student.user for student in students]
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    print(students)
    return render(request, "hod_template/manage_student.html", context)

def delete_student(request, student_id):
    # Retrieve the student object to be deleted
    student = get_object_or_404(User, id=student_id)
    # print(student)

    
    print("sdfsd")
        # Check if the student is not a tutor (isTutor=0) before deleting
    student.delete()
            
        # Redirect to a success page or another appropriate view
      # Change 'students_list' to the URL name of the page you want to redirect to

    # Render a confirmation page (optional)
    return render(request, 'hod_template/manage_student.html', {'student': student})


def view_catgories(request):
    course = category.objects.all()
    wishlist_count = 0
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    return render(request, 'hod_template/tutor_course_enroll.html', {'courses': course,'wishlist_count': wishlist_count})

    
        # .........COURSE MANAGING...............

def filtered_course_list(request, category_name):
    # Get the category object based on the category_id
    ccategory = get_object_or_404(category, name=category_name)
    wishlist_count = 0
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    # Filter courses based on the category object
    courses = CourseDetail.objects.filter(course=ccategory, is_active=True)
   


    context = {
        
        'category': ccategory,
        'courses': courses,
        'category_name':category_name,
        'wishlist_count': wishlist_count
    }   
    print(ccategory)

    return render(request, 'tutor_template/course_list.html', context)

@login_required
def manage_tutor_courses(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        action = request.POST.get('action')

        if action in ['activate', 'deactivate']:
            course = get_object_or_404(CourseDetail, pk=course_id)

            if action == 'activate':
                course.is_active = True
                message = 'Course activated successfully'
            elif action == 'deactivate':
                course.is_active = False
                message = 'Course deactivated successfully'
            
            course.save()
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    # Retrieve all CourseDetail objects
    all_courses = CourseDetail.objects.all()

    # Create a Paginator object with 6 entries per page
    paginator = Paginator(all_courses, 6)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    courses = paginator.get_page(page_number)

    context = {
        'courses': courses,
    }

    return render(request, 'hod_template/manage_tutor_courses.html', context)
  

 # .........END COURSE MANAGING...............

def manage_subject(request):
  
    return render(request, "hod_template/manage_subject.html", context={})


def edit_student(request, student_id):

         return render(request, "hod_template/edit_student_template.html", context={})




def admin_view_profile(request):
    
    return render(request, "hod_template/admin_view_profile.html", context={})

@login_required
def edit_admin_profile(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        # Update the user's data
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Handle profile picture upload
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile = UserProfile.objects.get(user=user)
            UserProfile.profile_picture = profile_picture
            user_profile.save()            
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('admin_view_profile')

    return render(request, 'hod_template/admin_view_profile.html', {'user': user})





import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Sample function to generate a line chart for payments including price
def generate_payments_line_chart(request):
    # Retrieve payment data
    payments_data = Enrollment.objects.filter(is_active=True).count()

    # Prepare context
    context = {
        'page_title': 'Payments Line Chart',
        'payments_data': payments_data,
    }

    # Render the template with context
    return render(request, 'hod_template/payment.html', context)

# def delete_student(request, learner_id):
#     student = get_object_or_404(UserProfile, id=learner_id, isTutor=0)
   
#     if request.method == 'POST':
#         student.user.delete()  # Delete the associated User object
        
#         return redirect('success_page')  # Replace 'success_page' with the actual URL
    
#     return render(request, 'confirm_student_deletion.html', {'student': student})
