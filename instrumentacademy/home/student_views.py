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
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

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
            # profile_form.profile_picture=request.FILES['profile_picture']
            user_profile.save()  # Save the UserProfile
            
            user.save()
            profile.save()  # Save the User
            
            return render(request, 'student_template/studentprofile.html')
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)


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

from django.db.models import Q


@csrf_exempt
def student_view_attendance(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        start_date = request.POST.get('start_date')
        
        # Ensure course_id is a valid integer
        if course_id and course_id.isdigit():
            # Convert course_id to an integer
            course_id = int(course_id)
            
            # Filter the Attendance queryset based on course_id and start_date
            attendances = Attendance.objects.filter(
                Q(learner=request.user) & Q(class_schedule__course__id=course_id) & Q(class_schedule__start_datetime__date=start_date)
            )

            context = {
                'page_title': 'View Attendance',
                'courses': CourseDetail.objects.all(),  # Replace with your course model
                'attendance_data': attendances,
                  'selected_course_id': course_id,
            'selected_start_date': start_date,
            }
            return render(request, 'student_template/attendance_view.html', context)
        else:
            # Handle the case where course_id is not a valid integer
            return HttpResponse("Invalid course ID provided.")
    
    context = {
        'page_title': 'View Attendance',
        'courses': CourseDetail.objects.all(),  # Replace with your course model
        'attendance_data': None,
    }
    return render(request, 'student_template/attendance_view.html', context)

def course_material(request, course_id):
    course = get_object_or_404(CourseDetail, pk=course_id)
    modules = Module.objects.filter(course=course)
    lesson_materials = LessonMaterial.objects.filter(course=course) 
   
    res=True
    for lesson in lesson_materials:
        progress=Progress.objects.filter(learner=request.user,lesson_material=lesson)
        
        if progress:
            if not progress[0].is_completed:
                res=False
        else:
            res=False
    # print(a)
    video_lesson_materials = lesson_materials.filter(
        material_file__icontains='.mp4')  # You can customize the condition based on your file naming convention
    progress_list = Progress.objects.filter(learner=request.user, lesson_material__in=video_lesson_materials)


    context={
        'course': course,
        'modules': modules,
        'video_lesson_materials': video_lesson_materials,
        'progress':progress,  # Pass video lesson materials to the template
        'progress_list': progress_list,
    }
    if res:
        context['key']=True
    return render(request, 'student_template/course_materials.html', context)



@csrf_exempt  # For simplicity. You should handle CSRF properly in production.
def update_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        lesson_material_id = data.get('video_id')
        progress_percentage = data.get('progress_percentage')

        # Update the progress in your database
        try:
            print(lesson_material_id)
            progress_instance = Progress.objects.get(lesson_material_id=lesson_material_id,  learner=request.user)
            if progress_instance.progress_percentage < progress_percentage:
                progress_instance.progress_percentage = progress_percentage
                progress_instance.lesson_material_id = lesson_material_id
                progress_instance.save()
                if progress_percentage >= 90:
                    progress_instance.is_completed = True
                    progress_instance.save()
                    return JsonResponse({'message': 'Progress updated successfully'}, status=200)
            return JsonResponse({'message': 'Progress updated successfully'}, status=200)
        except Progress.DoesNotExist:
            Progress.objects.create(lesson_material_id=lesson_material_id, learner=request.user)  
            return JsonResponse({'message': 'Lesson material not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=400)



def get_progress(request):
    if request.method == 'GET':
        # Fetch necessary data from the request, you can modify this based on your actual model structure
        video_id = request.GET.get('video_id', None)
        print(video_id)
        if video_id is not None:
            try:
                # Assuming you have a model named YourModel with a field progress_percentage
                progress_instance = Progress.objects.get(lesson_material_id=video_id, learner=request.user)
                progress_percentage = progress_instance.progress_percentage
                return JsonResponse({'progress_percentage': progress_percentage}, status=200)
            except Progress.DoesNotExist:
                return JsonResponse({'message': 'Video not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


# def student_quiz(request):



#     return render(request,'student_template/student_quiz.html')

from django.http import JsonResponse
@csrf_exempt
def student_quiz(request, course_id):
    if request.method == 'POST':
        try:
            course = CourseDetail.objects.get(pk=course_id)
            questions = Question.objects.filter(course=course, is_active=True)

            # Retrieve user's responses from the request
            print("heelooo")
            data = json.loads(request.body.decode('utf-8'))

            user_responses = data.get('responseData')
            
            print(user_responses)

            # Calculate the score based on user's responses

            # Save the user's score to the database or any other necessary action
            # Example: Assuming there is a UserProfile model linked to User
            if user_responses:
                print("hiiii")
                    
                    # Iterate through user responses and save them
                question_id = user_responses.get('questionId')
                option_id = user_responses.get('selectedOption')
                is_correct = user_responses.get('isCorrect')
                print(question_id)

                # Save the response to the database
                response = Response.objects.create(
                    user=request.user,
                    course=course,
                    question_id=question_id,
                    option_id=option_id,
                    score=is_correct
                )
                print(response)
                response.save()

                return JsonResponse({'success': 'Quiz submitted successfully'})


            return JsonResponse({'success': 'Quiz submitted successfully', 'score': score})

        except CourseDetail.DoesNotExist:
            return JsonResponse({'error': 'Course not found'})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        try:
            course = CourseDetail.objects.get(pk=course_id)
            questions = Question.objects.filter(course=course, is_active=True)

            # Serialize questions data to JSON
            questions_data = []
            for question in questions:
                question_data = {
                    'id': question.id,
                    'title': question.title,
                    'options': list(question.options.values('id','text', 'is_correct'))
                }
                questions_data.append(question_data)

            questions_json = json.dumps({'course': course.name, 'questions': questions_data})   
            return render(request, 'student_template/student_quiz.html', {'questions_json': questions_json, 'course': course})

        except CourseDetail.DoesNotExist:
            return JsonResponse({'error': 'Course not found'})

        except Exception as e:
            return JsonResponse({'error': str(e)})







import pdfkit
from django.template import Context, loader

def generate_certificate(request, course_id):
    # Fetch course details, user name, and other required data
    course = CourseDetail.objects.get(pk=course_id)
    user = request.user
    existing_certificate = Certificate.objects.filter(user=user, course=course).first()

    if existing_certificate:
        # If a certificate already exists, return it without creating a new one
        return existing_certificate
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Create and save the certificate in the database
    certificate = Certificate(user=user, course=course, issued_date=current_date)
    certificate.save()

    return certificate

def view_certificate(request, course_id):

    course = CourseDetail.objects.get(pk=course_id)  # Adjust this based on your models
    #current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    certificate = generate_certificate(request, course_id)
    if isinstance(certificate, HttpResponse):
        return certificate  
    context = {
        'course': certificate.course,
        'current_date': certificate.issued_date.strftime("%Y-%m-%d"),
        'user': certificate.user,
        'certificate_id': certificate.id ,
    }
    
    return render(request, 'student_template/download_certificate.html', context)



def download_certificate(request, certificate_id):

    certificate = get_object_or_404(Certificate, pk=certificate_id)


    # Load the HTML template as a Django template
    template = loader.get_template('student_template/download_certificate.html')

    # Define the context as a dictionary
    print(certificate.id)
    context = {
        'user': certificate.user,
        'course': certificate.course,
        'current_date': certificate.issued_date.strftime("%Y-%m-%d"),
        'certificate':certificate,
        'download':True
    }

    # Render the template with the context
    rendered_html = template.render(context)

    # Create a PDF response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{certificate.user.username}_certificate.pdf"'

    # Specify the path to wkhtmltopdf executable in a list of options
    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'quiet': '',  # Disable wkhtmltopdf console output
    }

    # Generate the PDF from the HTML content using pdfkit with the config
    pdf_data = pdfkit.from_string(rendered_html, False, options=pdfkit_options, configuration=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'))

    # Write the PDF data to the response
    response.write(pdf_data)

    return response



def student_feedback(request):
   
    return render(request, "student_template/student_feedback.html")

def student_view_notification(request):
  
    return render(request, "student_template/student_view_notification.html")

def student_view_result(request):
   
    return render(request, "student_template/student_view_result.html")
