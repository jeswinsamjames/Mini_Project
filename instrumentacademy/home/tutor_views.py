import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.shortcuts import render, Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


def tutor_home(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # total_students = Student.objects.filter(course=tutor.course).count()
    # total_leave = LeaveReporttutor.objects.filter(tutor=tutor).count()
    # subjects = Subject.objects.filter(tutor=tutor)
    # total_subject = subjects.count()
    # attendance_list = Attendance.objects.filter(subject__in=subjects)
    # total_attendance = attendance_list.count()
    # attendance_list = []
    # subject_list = []
    # for subject in subjects:
    #     attendance_count = Attendance.objects.filter(subject=subject).count()
    #     subject_list.append(subject.name)
    #     attendance_list.append(attendance_count)
    # context = {
    #     'page_title': 'tutor Panel - ' + str(tutor.admin.last_name) + ' (' + str(tutor.course) + ')',
    #     'total_students': total_students,
    #     'total_attendance': total_attendance,
    #     'total_leave': total_leave,
    #     'total_subject': total_subject,
    #     'subject_list': subject_list,
    #     'attendance_list': attendance_list
    # }
    return render(request, 'tutor_template/home_content.html')

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
            user_profile.description = request.POST['description']
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
    courses = CourseDetail.objects.all()
    print(courses)
    return render(request, 'tutor_template/course_list.html', {'courses': courses})

def tutor_take_attendance(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # subjects = Subject.objects.filter(tutor_id=tutor)
    # sessions = Session.objects.all()
    # context = {
    #     'subjects': subjects,
    #     'sessions': sessions,
    #     'page_title': 'Take Attendance'
    # }

    return render(request, 'tutor_template/tutor_take_attendance.html')


# @csrf_exempt
# def get_students(request):
#     subject_id = request.POST.get('subject')
#     session_id = request.POST.get('session')
#     try:
#         subject = get_object_or_404(Subject, id=subject_id)
#         session = get_object_or_404(Session, id=session_id)
#         students = Student.objects.filter(
#             course_id=subject.course.id, session=session)
#         student_data = []
#         for student in students:
#             data = {
#                     "id": student.id,
#                     "name": student.admin.last_name + " " + student.admin.first_name
#                     }
#             student_data.append(data)
#         return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
#     except Exception as e:
#         return e



# @csrf_exempt
# def save_attendance(request):
#     student_data = request.POST.get('student_ids')
#     date = request.POST.get('date')
#     subject_id = request.POST.get('subject')
#     session_id = request.POST.get('session')
#     students = json.loads(student_data)
#     try:
#         session = get_object_or_404(Session, id=session_id)
#         subject = get_object_or_404(Subject, id=subject_id)

#         # Check if an attendance object already exists for the given date and session
#         attendance, created = Attendance.objects.get_or_create(session=session, subject=subject, date=date)

#         for student_dict in students:
#             student = get_object_or_404(Student, id=student_dict.get('id'))

#             # Check if an attendance report already exists for the student and the attendance object
#             attendance_report, report_created = AttendanceReport.objects.get_or_create(student=student, attendance=attendance)

#             # Update the status only if the attendance report was newly created
#             if report_created:
#                 attendance_report.status = student_dict.get('status')
#                 attendance_report.save()

#     except Exception as e:
#         return None

#     return HttpResponse("OK")


def tutor_update_attendance(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # subjects = Subject.objects.filter(tutor_id=tutor)
    # sessions = Session.objects.all()
    # context = {
    #     'subjects': subjects,
    #     'sessions': sessions,
    #     'page_title': 'Update Attendance'
    # }

    return render(request, 'tutor_template/tutor_update_attendance.html')


# @csrf_exempt
# def get_student_attendance(request):
#     attendance_date_id = request.POST.get('attendance_date_id')
#     try:
#         date = get_object_or_404(Attendance, id=attendance_date_id)
#         attendance_data = AttendanceReport.objects.filter(attendance=date)
#         student_data = []
#         for attendance in attendance_data:
#             data = {"id": attendance.student.admin.id,
#                     "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
#                     "status": attendance.status}
#             student_data.append(data)
#         return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
#     except Exception as e:
#         return e


# @csrf_exempt
# def update_attendance(request):
#     student_data = request.POST.get('student_ids')
#     date = request.POST.get('date')
#     students = json.loads(student_data)
#     try:
#         attendance = get_object_or_404(Attendance, id=date)

#         for student_dict in students:
#             student = get_object_or_404(
#                 Student, admin_id=student_dict.get('id'))
#             attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
#             attendance_report.status = student_dict.get('status')
#             attendance_report.save()
#     except Exception as e:
#         return None

#     return HttpResponse("OK")


# def tutor_apply_leave(request):
#     form = LeaveReporttutorForm(request.POST or None)
#     tutor = get_object_or_404(tutor, admin_id=request.user.id)
#     context = {
#         'form': form,
#         'leave_history': LeaveReporttutor.objects.filter(tutor=tutor),
#         'page_title': 'Apply for Leave'
#     }
#     if request.method == 'POST':
#         if form.is_valid():
#             try:
#                 obj = form.save(commit=False)
#                 obj.tutor = tutor
#                 obj.save()
#                 messages.success(
#                     request, "Application for leave has been submitted for review")
#                 return redirect(reverse('tutor_apply_leave'))
#             except Exception:
#                 messages.error(request, "Could not apply!")
#         else:
#             messages.error(request, "Form has errors!")
#     return render(request, "tutor_template/tutor_apply_leave.html", context)


def tutor_feedback(request):
    # form = FeedbacktutorForm(request.POST or None)
    # tutor = get_object_or_404(tutor, admin_id=request.user.id)
    # context = {
    #     'form': form,
    #     'feedbacks': Feedbacktutor.objects.filter(tutor=tutor),
    #     'page_title': 'Add Feedback'
    # }
    # if request.method == 'POST':
    #     if form.is_valid():
    #         try:
    #             obj = form.save(commit=False)
    #             obj.tutor = tutor
    #             obj.save()
    #             messages.success(request, "Feedback submitted for review")
    #             return redirect(reverse('tutor_feedback'))
    #         except Exception:
    #             messages.error(request, "Could not Submit!")
    #     else:
    #         messages.error(request, "Form has errors!")
    return render(request, "tutor_template/tutor_feedback.html")


def tutor_view_profile(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # form = tutorEditForm(request.POST or None, request.FILES or None,instance=tutor)
    # context = {'form': form, 'page_title': 'View/Update Profile'}
    # if request.method == 'POST':
    #     try:
    #         if form.is_valid():
    #             first_name = form.cleaned_data.get('first_name')
    #             last_name = form.cleaned_data.get('last_name')
    #             password = form.cleaned_data.get('password') or None
    #             address = form.cleaned_data.get('address')
    #             gender = form.cleaned_data.get('gender')
    #             passport = request.FILES.get('profile_pic') or None
    #             admin = tutor.admin
    #             if password != None:
    #                 admin.set_password(password)
    #             if passport != None:
    #                 fs = FileSystemStorage()
    #                 filename = fs.save(passport.name, passport)
    #                 passport_url = fs.url(filename)
    #                 admin.profile_pic = passport_url
    #             admin.first_name = first_name
    #             admin.last_name = last_name
    #             admin.address = address
    #             admin.gender = gender
    #             admin.save()
    #             tutor.save()
    #             messages.success(request, "Profile Updated!")
    #             return redirect(reverse('tutor_view_profile'))
    #         else:
    #             messages.error(request, "Invalid Data Provided")
                return render(request, "tutor_template/tutor_view_profile.html")
    #     except Exception as e:
    #         messages.error(
    #             request, "Error Occured While Updating Profile " + str(e))
    #         return render(request, "tutor_template/tutor_view_profile.html", context)

    # return render(request, "tutor_template/tutor_view_profile.html", context)


# @csrf_exempt
# def tutor_fcmtoken(request):
#     token = request.POST.get('token')
#     try:
#         tutor_user = get_object_or_404(CustomUser, id=request.user.id)
#         tutor_user.fcm_token = token
#         tutor_user.save()
#         return HttpResponse("True")
#     except Exception as e:
#         return HttpResponse("False")


def tutor_view_notification(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # notifications = Notificationtutor.objects.filter(tutor=tutor)
    # context = {
    #     'notifications': notifications,
    #     'page_title': "View Notifications"
    # }
    return render(request, "tutor_template/tutor_view_notification.html")


def tutor_add_result(request):
    # tutor = get_object_or_404(tutor, admin=request.user)
    # subjects = Subject.objects.filter(tutor=tutor)
    # sessions = Session.objects.all()
    # context = {
    #     'page_title': 'Result Upload',
    #     'subjects': subjects,
    #     'sessions': sessions
    # }
    # if request.method == 'POST':
    #     try:
    #         student_id = request.POST.get('student_list')
    #         subject_id = request.POST.get('subject')
    #         test = request.POST.get('test')
    #         exam = request.POST.get('exam')
    #         student = get_object_or_404(Student, id=student_id)
    #         subject = get_object_or_404(Subject, id=subject_id)
    #         try:
    #             data = StudentResult.objects.get(
    #                 student=student, subject=subject)
    #             data.exam = exam
    #             data.test = test
    #             data.save()
    #             messages.success(request, "Scores Updated")
    #         except:
    #             result = StudentResult(student=student, subject=subject, test=test, exam=exam)
    #             result.save()
    #             messages.success(request, "Scores Saved")
    #     except Exception as e:
    #         messages.warning(request, "Error Occured While Processing Form")
    return render(request, "tutor_template/tutor_add_result.html")

def EditResultView(request):
    return render(request,'edit_student_result.html')


# @csrf_exempt
# def fetch_student_result(request):
#     try:
#         subject_id = request.POST.get('subject')
#         student_id = request.POST.get('student')
#         student = get_object_or_404(Student, id=student_id)
#         subject = get_object_or_404(Subject, id=subject_id)
#         result = StudentResult.objects.get(student=student, subject=subject)
#         result_data = {
#             'exam': result.exam,
#             'test': result.test
#         }
#         return HttpResponse(json.dumps(result_data))
#     except Exception as e:
#         return HttpResponse('False')
