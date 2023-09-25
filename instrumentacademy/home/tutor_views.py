import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.shortcuts import render, Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import *
from .models import *


def tutor_home(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # total_students = Student.objects.filter(course=tutor.course).count()
    tutors_with_learner_and_course_count = UserProfile.objects.filter(isTutor=0).annotate(
    learner_count=Count('user__enrollment__learner', distinct=True),
    course_count=Count('user__courses', distinct=True)
    )

    context = {
        'tutors_with_learner_and_course_count': tutors_with_learner_and_course_count,
    }
    return render(request, 'tutor_template/home_content.html',context)

@login_required
def view_profile_tutor(request):
    user = request.user
    try:
        user_profile = user.userprofile  # Assuming the related name is 'userprofile'
    except UserProfile.DoesNotExist:
        return redirect('login') 

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'tutor_template/tutorprofile.html', context)
@login_required
def edit_profile_tutor(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Access the UserProfile object associated with the User
            user_profile = UserProfile.objects.get(user=user)

            # Update gender, address, first name, and last name
            user_profile.gender = request.POST['gender']
            user_profile.address = request.POST['address']
            user_profile.specialist = request.POST['specialist']
            user_profile.phoneNo = request.POST['phoneNo']

            # Handle teaching experience as a string with "year(s)"
            user_profile.teaching_experience = request.POST['teaching_experience']
            user.last_name = request.POST['last_name']
            user.first_name = request.POST['first_name']
            
            # Handle profile picture
            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            
            user_profile.save()  # Save the UserProfile
            user.save()  # Save the User

            return redirect('view_profile_tutor')
    else:
        form = EditProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    
    return render(request, 'tutor_template/tutorprofile.html', context)

                        # .......COURSES VIEW..........
@login_required
def create_course(request):
     if request.method == 'POST':
        # Get the form data from the request
        name = request.POST['name']
        instrument_name = request.POST['instrument_name']
        description = request.POST['description']
        years_of_experience = request.POST['years_of_experience']
        is_active = True if request.POST.get('is_active') else False

        # Handle the uploaded course image
        course_image = request.FILES.get('course_image')
        # Create a new category object based on the selected instrument_name
        try:
            category_obj = category.objects.get(instrument_name=instrument_name)
        except category.DoesNotExist:
            category_obj = None

        if not category_obj:
            # Handle the case where the selected instrument_name doesn't exist in the Category model
            messages.error(request, 'Invalid instrument name selected.')
            return redirect('create_course')

        # Create a new course object
        course = CourseDetail(
            name=name,
            course=category_obj,  # Use the category_obj as the course_type
            description=description,
            years_of_experience=years_of_experience,
            is_active=is_active,
            image=course_image,
            tutor=request.user
        )

        # Save the course object to the database
        course.save()

        # Redirect to a success page or course listing
        messages.success(request, 'Course created successfully!')
        return redirect('course_list')

    
     return render(request, 'tutor_template/create_course.html')




@login_required
def course_list(request):
    active_courses = CourseDetail.objects.filter(is_active=False)
    context = {
        'courses': active_courses,
        'page_title': 'Manage Courses',
    }
    return render(request, 'tutor_template/course_list.html', context)

def manage_courses(request):
    courses = CourseDetail.objects.filter(tutor=request.user)  # Retrieve all courses
    context = {'courses': courses, 'page_title': 'Manage Courses'}
    return render(request, 'tutor_template/manage_course.html', context)

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Ensure that only the tutor who created the course can edit it
    if request.user == course.tutor:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('manage_courses')  # Redirect to the tutor's dashboard
        else:
            form = CourseForm(instance=course)

        return render(request, 'tutor_template/edit_course_tutor.html', {'form': form, 'course': course})
    else:
        # Handle unauthorized access (e.g., redirect to an error page)
        pass

from django.http import HttpResponseForbidden
def delete_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Ensure that only the tutor who created the course can delete it
    if request.user == course.tutor:
        course.delete()
        messages.success(request, 'Course has been deleted successfully.')
        return redirect('manage_courses')  # Redirect to the tutor's dashboard
    else:
        # Handle unauthorized access (e.g., redirect to an error page)
        return HttpResponseForbidden("You are not authorized to delete this course.because this course is created by other tutor")
def activate_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Ensure that only the tutor who created the course can activate it
    if request.user == course.tutor:
        course.is_active = True
        course.save()
        return redirect('manage_courses')  # Redirect to the tutor's dashboard
    else:
        # Handle unauthorized access (e.g., redirect to an error page)
        pass

def deactivate_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Ensure that only the tutor who created the course can deactivate it
    if request.user == course.tutor:
        course.is_active = False
        course.save()
        return redirect('manage_courses')  
    else:
        
        pass
                    # ...........END COURSE.............


            # ........... COURSE Enroll.............

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    learner = request.user
    tutor=UserProfile.objects.filter(user=learner).first()
    if tutor.isTutor ==2:
         messages.error(request, 'Tutor login can\'t enroll in courses')
    elif Enrollment.objects.filter(learner=learner, course=course).exists():
       messages.warning(request, 'You are already enrolled in this course.')
        
    else:
        enrollment = Enrollment(learner=learner, course=course)
        enrollment.save()
        messages.success(request, 'Enrollment successful.')

    return render(request, 'tutor_template/course_list.html',{'course': course})


def enrolled_courses_list(request):
    enrolled_courses = CourseDetail.objects.filter(tutor=request.user, is_active=True)
    active_courses = CourseDetail.objects.filter(is_active=True)
    context = {
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'tutor_template/enrolled_course_list.html', context)



def enrolled_course_details(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    enrolled_students = Enrollment.objects.filter(course=course)
    context = {
        'course': course,
        'enrolled_students': enrolled_students,
    }
    return render(request, 'tutor_template/enrolled_course_detail.html', context)

# @user_passes_test(lambda u: u.userprofile.isTutor == 2)  # Only allow tutors
def toggle_course_status(request, course_id):
    action = request.GET.get('action')  # Get the action from the query parameter

    course = get_object_or_404(CourseDetail, pk=course_id)

    if action == 'activate':    
        course.is_active = True
    elif action == 'deactivate':
        course.is_active = False

    course.save()
    
    return redirect('course_list')

 # ........... END COURSE Enroll.............

def add_module_and_lesson_material(request, course_id):
    # Retrieve the course based on the provided course_id
    course = get_object_or_404(CourseDetail, pk=course_id)

    if request.method == 'POST':
        module_form = ModuleForm(request.POST)
        lesson_material_form = LessonMaterialForm(request.POST, request.FILES,course_id=course_id)

        if module_form.is_valid():
            # Set the course for the module before saving
            module = module_form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Module created successfully.')
            return redirect('add_module_and_lesson_material', course_id=course.id)

        if lesson_material_form.is_valid():
            # Set the course for the lesson material before saving
            lesson_material = lesson_material_form.save(commit=False)
            lesson_material.course = course
            lesson_material.save()
            messages.success(request, 'Lesson created successfully.')

            return redirect('add_module_and_lesson_material',course_id=course.id)

    else:
        module_form = ModuleForm()
        lesson_material_form = LessonMaterialForm(course_id=course_id)

    return render(request, 'tutor_template/upload_lesson_material.html', {
        'course': course,  # Pass the course to the template
        'module_form': module_form,
        'lesson_material_form': lesson_material_form,
    })
def tutor_course_content(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    modules = Module.objects.filter(course=course)
    lesson_materials = LessonMaterial.objects.filter(course=course)

    video_lesson_materials = lesson_materials.filter(
        material_file__icontains='.mp4')  # You can customize the condition based on your file naming convention
    print(modules)
    # Render the course content template with the course, modules, and video lesson materials
    return render(request, 'tutor_template/view_lesson_materials.html', {
        'course': course,
        'modules': modules,
        'video_lesson_materials': video_lesson_materials,  # Pass video lesson materials to the template
    })





#////////////////////////////
def tutor_take_attendance(request):
   
    return render(request, 'tutor_template/tutor_take_attendance.html')




def tutor_update_attendance(request):

    return render(request, 'tutor_template/tutor_update_attendance.html')


def tutor_feedback(request):
    return render(request, "tutor_template/tutor_feedback.html")


def tutor_view_profile(request):

 return render(request, "tutor_template/tutor_view_profile.html")
  




def tutor_view_notification(request):
    
    return render(request, "tutor_template/tutor_view_notification.html")


def tutor_add_result(request):
   
    return render(request, "tutor_template/tutor_add_result.html")

def EditResultView(request):
    return render(request,'edit_student_result.html')

