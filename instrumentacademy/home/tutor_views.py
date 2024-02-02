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
from django.template.loader import render_to_string
from datetime import timedelta, datetime,timezone
from django.utils import timezone
from django.views.decorators.cache import cache_control





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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
                user_profile.save()
                user.save()
                
            if 'resume' in request.FILES:
                user_profile.resume = request.FILES['resume']
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
        amount = request.POST['amount']

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
            amount=amount,
            tutor=request.user
        )

        # Save the course object to the database
        course.save()

        # Redirect to a success page or course listing
        messages.success(request, 'Course created successfully!')
        return redirect('course_list')

     c=category.objects.all()
     context={
         'categories':c
     }
     return render(request, 'tutor_template/create_course.html',context)




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
def activate_course(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    course.is_active = True
    course.save()
    return redirect('/manage-courses/')

 # ........... END COURSE Enroll.............

 # ........... LESSON MATERIAL.............

def add_module_and_lesson_material(request, course_id):
    # Retrieve the course based on the provided course_id4
    print(course_id)
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


def list_modules(request):
    courses = CourseDetail.objects.filter(tutor=request.user, is_active=True)
 
    return render(request, 'tutor_template/manage_modules_lessons.html', {'courses':courses})

def module_list_view(request, course_id):
    # Get the course object or return a 404 error if it doesn't exist
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Retrieve modules and lessons related to the course
    modules = Module.objects.filter(course=course)
   
    lessons = LessonMaterial.objects.filter(module__course=course)
    print(lessons)

    context = {
        'course': course,
        'modules': modules,
        'lessons': lessons,
    }

    return render(request, 'tutor_template/view_modules.html', context)

def edit_module(request, module_id):
    module = get_object_or_404(Module, pk=module_id)

    if request.method == 'POST':
        module_form = ModuleForm(request.POST, instance=module)
        if module_form.is_valid():
            module_form.save()
            messages.success(request, 'updated successfully.')

            return redirect(reverse('module_list_view', args=[module.course.id]))  # Redirect to module_list_view with course_id
    else:
        module_form = ModuleForm(instance=module)

    return render(request, 'tutor_template/module_edit_form.html', {'module_form': module_form, 'module': module})

def delete_module(request, module_id):

    try:
        module = get_object_or_404(Module, pk=module_id)
        module.delete()
        messages.success(request, 'deleted successfully.')

        return HttpResponseRedirect(reverse('module_list_view', args=[module.course.id]))
    except LessonMaterial.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Lesson not found'})




def lesson_edit_page(request, lesson_id):
    try:
        lesson = LessonMaterial.objects.get(pk=lesson_id)
    except LessonMaterial.DoesNotExist:
        return redirect('some_error_view')

    if request.method == 'POST':
        form = LessonMaterialForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'updated successfully.')

            return redirect(reverse('module_list_view', args=[lesson.course.id]))  # Redirect to module_list_view with course_id
    else:
        form = LessonMaterialForm(instance=lesson)
        form.fields['module'].queryset = Module.objects.filter(course=lesson.module.course)


    context = {
        'form': form,
        'lesson': lesson,
    }

    return render(request, 'tutor_template/lesson_edit_form.html', context)
# Delete lesson view
def delete_lesson(request, lesson_id):
    try:
        lesson = LessonMaterial.objects.get(pk=lesson_id)
        lesson.delete()
        messages.success(request, 'deleted successfully.')

        return JsonResponse({'success': True})
    except LessonMaterial.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Lesson not found'})
    return render()



# def quiz_form(request):
#     if request.method == 'POST':
        
#         # Handle form submission and save question
#         question_title = request.POST.get('question-title')
#         print("question_title")
#         new_question = Question.objects.create(title=question_title)

#         for key, value in request.POST.items():
#             if key.startswith('option-'):
#                 Option.objects.create(question=new_question, text=value)

#         # Redirect to the quiz form page after saving a question
#         return redirect('quiz_form')

#     # Display the quiz form
#     questions = Question.objects.all()
#     return render(request, 'tutor_template/quiz.html', {'questions': questions})
from django.core.serializers import serialize

@csrf_exempt
def quiz_form(request, course_id):
    try:
        course = CourseDetail.objects.get(pk=course_id)
    except CourseDetail.DoesNotExist:
        return render(request, 'tutor_template/error.html', {'error_message': 'Course not found'})
    
    if request.method == 'POST':
        try:
            # Check if the form is for updating an existing question
            question_id = request.POST.get('question_id')
            if question_id:
                question = Question.objects.get(pk=question_id)
                question.title = request.POST.get('question-title')
                question.save()

                # Delete existing options for the question
                question.options.all().delete()

                # Update options for the question
                for key, value in request.POST.items():
                    if key.startswith('option-'):
                        option = Option(question=question, text=value)
                        option.save()
                        is_correct = request.POST.get('marked')

                        option.is_correct = 1 if key.endswith(is_correct) else 0
                        option.save()


                return JsonResponse({'success': True})
            # If it's a new question, create it
            else:
                question_title = request.POST.get('question-title')
                new_question = Question.objects.create(title=question_title, course=course)
                for key, value in request.POST.items():
                    if key.startswith('option-'):
                        is_correct = request.POST.get('marked')
                        Option.objects.create(
                            question=new_question,
                            text=value,
                            is_correct=1 if key.endswith(is_correct) else 0
                        )
                return redirect('quiz_form', course_id=course_id)
        except Exception as e:
            print(f"Error in quiz_form view (Form Submission): {e}")
            return render(request, 'tutor_template/quiz.html', {'error_message': f'An error occurred: {e}','course':course})
    
    # Fetch existing questions for the course
    questions = Question.objects.filter(course=course)
    
    # Serialize questions and options to JSON
    questions_json = json.dumps([
        {
            'pk': q.pk,
            'title': q.title,
            'options': [{'pk': option.pk, 'text': option.text, 'is_correct': option.is_correct} for option in q.options.all()]
        }
        for q in questions
    ])
    print(course.id)
    return render(request, 'tutor_template/quiz.html', {'questions': questions,'questions_json' : questions_json,'course':course})


 # ...........END LESSON MATERIAL.............


 # ...........class Scheduling.............



def course_schedule_class(request):
    courses = CourseDetail.objects.filter(tutor=request.user, is_active=True)
    return render(request, 'tutor_template/manage_schedule_class.html', {'courses':courses})
def upcoming_classes(request):
    upcoming_classes = ClassSchedule.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')
    return render(request, 'upcoming_classes.html', {'upcoming_classes': upcoming_classes})



@login_required

def tutor_schedule_class(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    if request.method == 'POST':
        form = ScheduleClassForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data['start_datetime']
            meeting_link = form.cleaned_data['meeting_link']
            description = form.cleaned_data['description']
            duration = form.cleaned_data['duration']

            if duration is not None:
                # Calculate the end time based on the start time and user-specified duration
                duration_hours = float(duration)
                duration_minutes = duration_hours * 60  # Convert to minutes
                end_datetime = start_datetime + timedelta(minutes=duration_minutes)  # Calculate end_datetime

                # Check if the current time is before or equal to the calculated end time
                current_datetime = timezone.now()

                if current_datetime <= end_datetime:
                    # Create a new class schedule associated with the specific course
                    class_schedule = ClassSchedule.objects.create(
                        course=course,
                        start_datetime=start_datetime,
                        meeting_link=meeting_link,
                        description=description,
                        duration=duration,
                    )
                    messages.success(request, 'Successfully scheduled')

                    # Create a notification for learners enrolled in the course
                    enrolled_learners = course.enrolled_learners.all()
                    for learner in enrolled_learners:
                        Notification.objects.create(
                            recipient=learner,
                            notification_type="Class Scheduled",
                            content=f'A new class for {course.name} has been scheduled.',
                        )

                    return redirect('course_schedule_class')
                else:
                    # The schedule has already ended, handle as needed
                    return redirect('expired_schedule_page')
            else:
                # Handle the case where no duration is provided
                # Create a new class schedule without an end time
                class_schedule = ClassSchedule.objects.create(
                    course=course,
                    start_datetime=start_datetime,
                    meeting_link=meeting_link,
                    description=description,
                )

                # Create a notification for learners enrolled in the course
                enrolled_learners = course.enrolled_learners.all()
                for learner in enrolled_learners:
                    Notification.objects.create(
                        recipient=learner,
                        notification_type="Class Scheduled",
                        content=f'A new class for {course.name} has been scheduled.',
                    )

                return redirect('course_schedule_class')
    else:
        form = ScheduleClassForm()

    return render(request, 'tutor_template/tutor_schedule_class.html', {'form': form, 'course': course})


@login_required
def view_scheduled_classes(request):
    current_datetime = datetime.now()
    tutor = request.user  # Get the currently logged-in tutor

    # Get upcoming classes for the logged-in tutor
    upcoming_classes = ClassSchedule.objects.filter(
        course__tutor=tutor,
        start_datetime__gt=current_datetime
    ).order_by('start_datetime')

    # Get ended classes for the logged-in tutor
    ended_classes = ClassSchedule.objects.filter(
        course__tutor=tutor,
        start_datetime__lte=current_datetime
    ).order_by('start_datetime')

    return render(request, 'tutor_template/view_scheduled_classes.html', {
        'upcoming_classes': upcoming_classes,
        'ended_classes': ended_classes,
    })


def delete_class_schedule(request, class_schedule_id):
    class_schedule = get_object_or_404(ClassSchedule, pk=class_schedule_id)

    class_schedule.delete()
    messages.success(request, 'Class schedule deleted successfully.')
    
    return redirect('view_scheduled_classes')

 # ...........End class Scheduling.............


 # ...........Attendence class Scheduling.............



def tutor_courses(request):
    # Retrieve courses associated with the currently logged-in tutor
    tutor = request.user
    courses = CourseDetail.objects.filter(tutor=tutor)

    return render(request, 'tutor_template/tutor_courses_attendence.html', {'courses': courses})

def view_course_sessions(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)

    # Retrieve class sessions for the selected course
    class_sessions = ClassSchedule.objects.filter(course=course)

    return render(request, 'tutor_template/view_course_sessions_attendece.html', {'course': course, 'class_sessions': class_sessions})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def take_attendance(request, session_id):
    class_session = get_object_or_404(ClassSchedule, pk=session_id)
    learners = class_session.course.enrolled_learners.all()

    # Get the IDs of learners marked as present in the database for this session
    present_learner_ids = list(
        Attendance.objects.filter(class_schedule=class_session, is_present=True).values_list('learner__id', flat=True)
    )

    if request.method == 'POST':
        present_learner_ids = request.POST.getlist('attendance')

        for learner in learners:
            learner_id = str(learner.id)
            is_present = learner_id in present_learner_ids

            # Check if attendance record already exists for this learner and session
            attendance_record, created = Attendance.objects.get_or_create(
                learner=learner,
                class_schedule=class_session,
                course=class_session.course
            )

            # Handle the case where 'is_present' field can be null
            if is_present:
                attendance_record.is_present = True
            elif is_present is False:
                attendance_record.is_present = False
            attendance_record.save()

        messages.success(request, "Attendance successfully marked")
        return redirect('take_attendance', session_id)

    return render(
        request,
        'tutor_template/mark_attendance.html',
        {'class_session': class_session, 'learners': learners, 'present_learner_ids': present_learner_ids}
    )
 # ...........Attendence class Scheduling.............

#////////////////////////////



def tutor_feedback(request):
    return render(request, "tutor_template/tutor_feedback.html")





