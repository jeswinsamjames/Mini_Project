import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import *




def profile(request):
    user = request.user
    print (user.email)
    context={
        'user':user,
    }
    return render(request,'student_template/profile.html',context)


@login_required
def view_profile_learner(request):
    user = request.user
    user_profile = user.userprofile  # Assuming the related name is 'userprofile'
    
    context = {
        'user_profile': user_profile,
    }
    
    return render(request, 'student_template/studentprofile.html', context)

@login_required
def edit_profile_learner(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            profile = profile_form.save(commit=False)
            # Access the UserProfile object associated with the User
            user_profile = UserProfile.objects.get(user=user)

            # Update gender, address, first name, and last name
            user_profile.gender = request.POST['gender']
            user_profile.address = request.POST['address']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            profile_form.profile_picture=request.FILES['profile_picture']
            user_profile.save()  # Save the UserProfile
            user.save()
            profile.save()  # Save the User

            return render(request, 'student_template/studentprofile.html')
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance=request.user)
        prof=UserProfile.objects.filter(user=request.user)
        profile_form = UserProfileForm(instance=prof[0])

    context = {
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'student_template/studentprofile.html', context)

def enrolled_courses_list_leaner(request):
    learner = request.user
    enrolled_courses = Enrollment.objects.filter(learner=learner)
    print(enrolled_courses) 

    context = {
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'student_template/My_learning.html', context)

def student_home(request):
    # student = get_object_or_404(Student, admin=request.user)
    # total_subject = Subject.objects.filter(course=student.course).count()
    # total_attendance = AttendanceReport.objects.filter(student=student).count()
    # total_present = AttendanceReport.objects.filter(student=student, status=True).count()
    # if total_attendance == 0:  # Don't divide. DivisionByZero
    #     percent_absent = percent_present = 0
    # else:
    #     percent_present = math.floor((total_present/total_attendance) * 100)
    #     percent_absent = math.ceil(100 - percent_present)
    # subject_name = []
    # data_present = []
    # data_absent = []
    # subjects = Subject.objects.filter(course=student.course)
    # for subject in subjects:
    #     attendance = Attendance.objects.filter(subject=subject)
    #     present_count = AttendanceReport.objects.filter(
    #         attendance__in=attendance, status=True, student=student).count()
    #     absent_count = AttendanceReport.objects.filter(
    #         attendance__in=attendance, status=False, student=student).count()
    #     subject_name.append(subject.name)
    #     data_present.append(present_count)
    #     data_absent.append(absent_count)
    # context = {
    #     'total_attendance': total_attendance,
    #     'percent_present': percent_present,
    #     'percent_absent': percent_absent,
    #     'total_subject': total_subject,
    #     'subjects': subjects,
    #     'data_present': data_present,
    #     'data_absent': data_absent,
    #     'data_name': subject_name,
    #     'page_title': 'Student Homepage'

    # }
    return render(request, 'student_template/home_content.html')


def tutor_course_content(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    modules = Module.objects.filter(course=course)
    lesson_materials = LessonMaterial.objects.filter(course=course)

    video_lesson_materials = lesson_materials.filter(
        material_file__icontains='.mp4')  # You can customize the condition based on your file naming convention
    print(modules)
    # Render the course content template with the course, modules, and video lesson materials
    return render(request, 'student_template/view_lesson_materials.html', {
        'course': course,
        'modules': modules,
        'video_lesson_materials': video_lesson_materials,  # Pass video lesson materials to the template
    })

# views.py


@login_required
def view_scheduled_classes_leaner(request):
    user = request.user
    enrolled_courses = CourseDetail.objects.filter(enrollment__learner=user)
    current_datetime = datetime.now()

    # Filter scheduled classes where start_datetime is in the future (upcoming classes)
    scheduled_classes = ClassSchedule.objects.filter(
        course__in=enrolled_courses,
        start_datetime__gt=current_datetime
    ).order_by('start_datetime')

    return render(request, 'student_template/view_scheduled_classes_leaner.html', {'enrolled_courses': enrolled_courses, 'scheduled_classes': scheduled_classes})

def student_view_attendance(request):
   
        return render(request, 'student_template/student_view_attendance.html')
   

def student_feedback(request):
   
    return render(request, "student_template/student_feedback.html")



def student_view_notification(request):
  
    return render(request, "student_template/student_view_notification.html")


def student_view_result(request):
   
    return render(request, "student_template/student_view_result.html")
