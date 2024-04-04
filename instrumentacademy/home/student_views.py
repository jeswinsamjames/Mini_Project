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
    wishlist_count = 0
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    print(enrolled_courses) 
    not_started_courses = []
    ongoing_courses = []
    completed_courses = []
    for enrollment in enrolled_courses:
        
        CourseDetail = enrollment.course
        progress = Progress.objects.filter(learner=learner, lesson_material__course=CourseDetail).first()

        if progress:
            if progress.is_completed:
                completed_courses.append(CourseDetail)
            else:
                ongoing_courses.append(CourseDetail)
        else:
            not_started_courses.append(CourseDetail)

    context = {
        'enrolled_courses': enrolled_courses,
        'not_started_courses': not_started_courses,
        'ongoing_courses': ongoing_courses,
        'completed_courses': completed_courses,
                'wishlist_count': wishlist_count,

    }
    return render(request, 'student_template/My_learning.html', context)

def student_home(request):
    # Retrieve student based on logged-in user
    student_profile = UserProfile.objects.get(user=request.user)

    # Retrieve total number of subjects for the student's course
    total_subjects = CourseDetail.objects.filter(tutor=student_profile.user).count()

    # Retrieve total attendance reports for the student
    total_attendance_reports = Attendance.objects.filter(learner=student_profile.user).count()

    # Retrieve total number of present attendances for the student
    total_present = Attendance.objects.filter(learner=student_profile.user, is_present=True).count()

    # Calculate percentage present and percentage absent
    if total_attendance_reports == 0:
        percent_absent = percent_present = 0
    else:
        percent_present = round((total_present / total_attendance_reports) * 100)
        percent_absent = 100 - percent_present

    # Initialize lists to store subject names, present data, and absent data
    subject_names = []
    data_present = []
    data_absent = []

    # Retrieve subjects for the student's course
    subjects = CourseDetail.objects.filter(tutor=student_profile.user)
    for subject in subjects:
        # Retrieve class schedules for the subject
        class_schedules = ClassSchedule.objects.filter(course=subject)
        
        # Count attendance records for the student in each class schedule
        attendance_count = Attendance.objects.filter(class_schedule__in=class_schedules, learner=student_profile.user).count()
        present_count = Attendance.objects.filter(class_schedule__in=class_schedules, learner=student_profile.user, is_present=True).count()
        absent_count = attendance_count - present_count
        
        # Append subject name and attendance data to respective lists
        subject_names.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    
    # Prepare context dictionary to pass data to template
    context = {
        'total_attendance': total_attendance_reports,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_subjects': total_subjects,
        'subjects': subjects,
        'data_present': data_present,
        'data_absent': data_absent,
        'subject_names': subject_names,
        'page_title': 'Student Homepage'
    }
    
    return render(request, 'student_template/home_content.html', context)


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
    questions = Question.objects.filter(course=course, is_active=True)
    user_responses = Response.objects.filter(user=request.user, question_id__in=questions.values_list('id', flat=True))
    total_active_questions = questions.count()
    total_user_responses = user_responses.count()
    all_questions_attempted = total_user_responses == total_active_questions and total_user_responses > 0 and total_active_questions > 0;
    res=True
    for lesson in lesson_materials:
        progress=Progress.objects.filter(learner=request.user,lesson_material=lesson)
        
        if progress:
            if not progress[0].is_completed:
                res=False
                message = "Content is being uploaded. Please check back later."

        else:
            res=False
            message = "Content is being uploaded. Please check back later."

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
        'all_questions_attempted': all_questions_attempted
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
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def student_quiz(request, course_id):
    if request.method == 'POST':
        try:
            course = CourseDetail.objects.get(pk=course_id)
            questions = Question.objects.filter(course=course, is_active=True)

            # Retrieve user's responses from the request
            data = json.loads(request.body.decode('utf-8'))
            user_responses = data.get('responseData')
            
            if user_responses:
                question_id = user_responses.get('questionId')
                option_id = user_responses.get('selectedOption')
                is_correct = user_responses.get('isCorrect')

                # Check if a response already exists for this user and question
                try:
                    response = Response.objects.get(user=request.user, question_id=question_id)
                    # Update the existing response with the new option selected by the user
                    response.option_id = option_id
                    response.score = is_correct
                    response.save()
                except ObjectDoesNotExist:
                    # If a response does not exist, create a new one
                    response = Response.objects.create(
                        user=request.user,
                        course=course,
                        question_id=question_id,
                        option_id=option_id,
                        score=is_correct
                    )
                user_responses = Response.objects.filter(user=request.user, course=course)

                total_attempted_questions = len(set(questions))
                print('Total attempts', total_attempted_questions)
                    
                    # Calculate the user's total score
                total_score = 0

                if user_responses:
                    active_responses = [response for response in user_responses if response.question.is_active]
                    total_score = sum(response.score for response in active_responses)
                    print('Total attempts', total_score)


                return JsonResponse({'success': 'Quiz response updated successfully', 'total_score': total_score,'total_attempted_questions': total_attempted_questions})

        except CourseDetail.DoesNotExist:
            return JsonResponse({'error': 'Course not found'})

        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        try:
            course = CourseDetail.objects.get(pk=course_id)
            questions = Question.objects.filter(course=course, is_active=True)
            print(questions)

            # Retrieve responses for the current user and course
            user_responses = Response.objects.filter(user=request.user, course=course)
            total_attempted_questions = len(set(questions))
            print('Total attempts', total_attempted_questions)
                    
                    # Calculate the user's total score
            total_score = 0

            if user_responses:
                active_responses = [response for response in user_responses if response.question.is_active]
                total_score = sum(response.score for response in active_responses)
                print('Total attempts', total_score)
            
           

 
            # Serialize questions data to JSON
            questions_data = []
            for question in questions:
                question_data = {
                    'id': question.id,
                    'title': question.title,
                    'options': list(question.options.values('id', 'text', 'is_correct'))
                }
                questions_data.append(question_data)

            questions_json = json.dumps({'course': course.name, 'questions': questions_data})   

            # Pass the user's total score and questions data to the template
            return render(request, 'student_template/student_quiz.html', {
                'questions_json': questions_json,
                'course': course,
                'user_responses': user_responses,
                'total_attempted_questions': total_attempted_questions,
                'total_score': total_score,
                
            })

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
    try:
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

    except OSError as e:
            # Handle the case of no internet connection
            error_message = 'Error generating PDF: No internet connection'
            return JsonResponse({'error': error_message}, status=500)
    
from django.db.models import Avg
from itertools import zip_longest

@login_required
def tutor_profile(request, course_id):
    course = get_object_or_404(CourseDetail, id=course_id)
    user_profile = get_object_or_404(UserProfile, user=course.tutor)

    # Retrieve rating and review data for the course
    try:
        rating_review = RatingReview.objects.get(course=course, user=request.user)
        rating = rating_review.rating
        review = rating_review.review
    except RatingReview.DoesNotExist:
        rating = None
        review = None

    comments = RatingReview.objects.filter(course=course)
    user_profiles = UserProfile.objects.filter(user__in=comments.values_list('user', flat=True))
    comment_user_pairs = zip_longest(comments, user_profiles)
    learner=request.user
    enrolled_courses = Enrollment.objects.filter(learner=learner)
    yes=None
    for i in enrolled_courses:
        if i.course==course:
            yes=True
    print(12356,enrolled_courses)

    context = {
        'course': course,
        'user_profile': user_profile,
        'rating': rating,
        'review': review,
        'comments': comments,
        'user_profiles': user_profiles,
        'comment_user_pairs': comment_user_pairs,
        'enrolled_courses': enrolled_courses,
        'yes':yes

    }
    return render(request, "student_template/tutor_profile.html", context)


def get_updated_rating(request, course_id):
    course = get_object_or_404(CourseDetail, id=course_id)
    ratings = RatingReview.objects.filter(course=course)
    num_ratings = RatingReview.objects.filter(course=course).count()
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    comments = RatingReview.objects.filter(course=course).values('user__username', 'review')
    comments_data = list(comments)
    return JsonResponse({
        'average_rating': average_rating,
        'num_ratings': num_ratings,
        'comments': comments_data,
    

    })


@login_required
def rating_review(request, course_id):
    course = get_object_or_404(CourseDetail, id=course_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        user = request.user

        # Check if the user has already submitted a rating and review for this course
        existing_rating_review = RatingReview.objects.filter(user=user, course=course).first()
        if existing_rating_review:
            # Update the existing rating and review
            existing_rating_review.rating = rating
            existing_rating_review.review = review
            existing_rating_review.save()
            # messages.success(request, 'Rating and review updated successfully.')
        else:
            # Create a new rating and review
            rating_review = RatingReview(user=user, course=course, rating=rating, review=review)
            rating_review.save()
            # messages.success(request, 'Rating and review posted successfully.')

        # Render the template with a success message
        context = {
            'course': course,
            'success_message': 'Rating and review posted successfully.'  # Add success message to the context
        }
        return render(request, 'student_template/tutor_profile.html', context)

    # Render the template without a success message for GET requests
    context = {
        'course': course,
    }
    return render(request, 'student_template/tutor_profile.html', context)


#..................................wishlist........................
def wishlist(request):
    if request.user.is_authenticated:
        wishlist = WishlistItem.objects.filter(user=request.user)
        wishlist_count = 0
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
        # Retrieve course ids from the wishlist items
        course_ids = [item.course.id for item in wishlist]
        # Retrieve course details based on the course ids
        courses = CourseDetail.objects.filter(pk__in=course_ids)
        return render(request, 'student_template/wishlist.html', {'wishlist': wishlist, 'courses': courses,'wishlist_count': wishlist_count,
})
    else:
        return redirect('login')  # Redirect to login page
    
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_to_wishlist(request, course_id):
    print("adedddd")
    # Get the course object based on the course_id
    course = CourseDetail.objects.get(pk=course_id)

    # Check if the course is already in the user's wishlist
    if WishlistItem.objects.filter(user=request.user, course=course).exists():
        # Course is already in the wishlist
        return JsonResponse({'message': 'Course is already in the wishlist'}, status=400)

    # Add the course to the user's wishlist
    wishlist_item = WishlistItem.objects.create(user=request.user, course=course)

    return JsonResponse({'message': 'Course added to wishlist successfully'}, status=200)

def remove_from_wishlist(request, course_id):
    if request.user.is_authenticated:
        try:
            # Get the wishlist item associated with the user and course
            wishlist_item = WishlistItem.objects.get(user=request.user, course_id=course_id)
            # Remove the course from the wishlist
            wishlist_item.delete()
            return JsonResponse({'message': 'Course removed from wishlist.'})
        except WishlistItem.DoesNotExist:
            return JsonResponse({'error': 'Wishlist item does not exist.'}, status=400)
        except CourseDetail.DoesNotExist:
            return JsonResponse({'error': 'Course does not exist.'}, status=400)
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

#..............................wiahlist/................................................................

import pytz
from django.utils import timezone
from datetime import timedelta

def view_assignments(request):
    # Get courses enrolled by the user (learner)
    enrolled_courses = request.user.enrolled_courses.all()
    assignments_by_course = {}
    ist = pytz.timezone('Asia/Kolkata')  # Indian Standard Time
    current_date = timezone.now().astimezone(ist)    
    print("curwent datetime", current_date)
    for course in enrolled_courses:
        current_datetime = timezone.now().astimezone(timezone.get_fixed_timezone(330))  # 330 minutes offset for IST
        current_datetime = current_datetime + timedelta(hours=5, minutes=30)

    # Get assignments uploaded by learners for the specified course taught by the tutor
        assignments = Assignments.objects.filter(course=course, is_active=True)

        # Loop through each assignment and check if its due date has passed
        for assignment in assignments:
            if assignment.due_date < current_datetime:
                assignment.ended = True  # Due date has passed
            else:
                assignment.ended = False  # Due date is in the future
        if assignments.exists():
            assignments_by_course[course] = assignments
    if request.method == 'POST':
        # Handle file upload for the selected assignment
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignments, pk=assignment_id)
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Save the uploaded file
            user_profile = request.user.userprofile
            course_id = assignment.course_id  # Get the course ID from the assignment
            assignment_file = UploadAssignment.objects.create(files=uploaded_file, assignment=assignment,user=request.user,user_profile=user_profile, course_id=course_id)
            assignment_file.save()
            messages.success(request, "File has been saved.")
            return redirect('view_assignments')
    for assignments in assignments_by_course.values():
        for assignment in assignments:
            assignment.uploaded_file = UploadAssignment.objects.filter(assignment=assignment).first()
    context = {'assignments_by_course': assignments_by_course, 'current_date': datetime.now()}
    return render(request, 'student_template/upload_assignment.html', context)





def delete_assignment_file(request, upload_assignment_id):
    assignment_file = get_object_or_404(UploadAssignment, pk=upload_assignment_id)
    assignment_file.files.delete()  # Delete the file from the storage
    assignment_file.delete()  # Delete the UploadAssignment instance
    
    return redirect('view_assignments') 














def student_feedback(request):
   
    return render(request, "student_template/student_feedback.html")

def student_view_notification(request):
  
    return render(request, "student_template/student_view_notification.html")

def student_view_result(request):
   
    return render(request, "student_template/student_view_result.html")
