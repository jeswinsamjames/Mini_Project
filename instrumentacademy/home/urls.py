from django.urls import path,include
from . import views,student_views,tutor_views,hod_views
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static
from .hod_views import PendingTutorListView, approve_tutor
urlpatterns = [
    
    path('', views.index,name='index'),
     path('custom-login/', views.custom_login, name='custom_login'),
    path('login', views.login,name='login'),
    path('homecontent', views.homecontent,name='homecontent'),
    path('index1', views.index1,name='index1'),
    path('logout', views.loggout,name='logout'),
    path('base', views.base),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('registration', views.registration,name="registration"), 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),

    path('search/', views.search_results, name='search_results'),
    path('metronome/', views.metronome, name='metronome'),
    
    


   


 #<<<<<<<<<<<<<<Student>>>>>>>>>>>>>>>

    
    path("logout_user/", views.logout_user, name='user_logout'),
    path("student/home/", student_views.student_home, name='student_home'),
    path('student/view/attendance/', student_views.student_view_attendance, name='student_view_attendance'),
    path("student/feedback/", student_views.student_feedback, name='student_feedback'),
#     path("student/fcmtoken/", student_views.student_fcmtoken,name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification, name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,name='student_view_result'),
    path('view_profile/learner/', student_views.view_profile_learner, name='view_profile_learner'),
    path('edit_profile/learner/', student_views.edit_profile_learner, name='edit_profile_learner'),
    path('mylearning/', student_views.enrolled_courses_list_leaner, name='mylearning'),
    path('tutor_course_content/<int:course_id>/', student_views.tutor_course_content, name='tutor_course_content'),
    path('scheduled-classes/', student_views.view_scheduled_classes_leaner, name='view_scheduled_classes_leaner'),
    path('course_material/<int:course_id>/', student_views.course_material, name='course_material'),
    path('update_progress/', student_views.update_progress, name='update_progress'),
    path('get_progress/', student_views.get_progress, name='get_progress'),
    path('student_quiz/<int:course_id>/', student_views.student_quiz, name='student_quiz'),

    path('view_certificate/<int:course_id>/', student_views.view_certificate, name='view_certificate'),
    path('generate_certificate/<int:course_id>/', student_views.generate_certificate, name='generate_certificate'),
    path('download_certificate/<int:certificate_id>/', student_views.download_certificate, name='download_certificate'),
    path('tutor_profile/<int:course_id>/',student_views.tutor_profile, name='tutor_profile'),




    #<<<<<<<<<<<<<<staff>>>>>>>>>>>>>>>

    path("tutor/home/", tutor_views.tutor_home, name='tutor_home'),
    path("tutor/feedback/", tutor_views.tutor_feedback, name='tutor_feedback'),
    path('edit_profile/tutor/', tutor_views.edit_profile_tutor, name='edit_profile_tutor'),
    path('view_profile/tutor/', tutor_views.view_profile_tutor, name='view_profile_tutor'),
    path('create-course/', tutor_views.create_course, name='create_course'),
    path('course-list', tutor_views.course_list, name='course_list'),
    path('manage-courses/', tutor_views.manage_courses, name='manage_courses'),  # for tutor course 
    path('edit-course/<int:course_id>/', tutor_views.edit_course, name='edit_course'),

    # Define the URL for the delete_course view with a dynamic course_id parameter
    path('delete-course/<int:course_id>/', tutor_views.delete_course, name='delete_course'),
    path('course/activate/<int:course_id>/', tutor_views.activate_course, name='activate_course'),
    path('course/deactivate/<int:course_id>/', tutor_views.deactivate_course, name='deactivate_course'),


     path('enroll/<int:course_id>/', tutor_views.enroll_course, name='enroll_course'),
     path('enrolled-courses/', tutor_views.enrolled_courses_list, name='enrolled_courses_list'),
     path('enrolled-course/<int:course_id>/', tutor_views.enrolled_course_details, name='enrolled_course_details'),
    # Activate a course
path('activate-course/<int:course_id>/', tutor_views.activate_course, name='activate_course'),


    # Deactivate a course
    path('toggle-course-status/<int:course_id>/', tutor_views.toggle_course_status, name='toggle_course_status'),


    path('add_module_and_lesson_material/<int:course_id>/', tutor_views.add_module_and_lesson_material, name='add_module_and_lesson_material'),
    path('list_modules/', tutor_views.list_modules, name='list_modules'),
    path('module_list_view/<int:course_id>/', tutor_views.module_list_view, name='module_list_view'),
    path('edit_module/<int:module_id>/', tutor_views.edit_module, name='edit_module'),
    path('delete_module/<int:module_id>/', tutor_views.delete_module, name='delete_module'),
    path('edit_lesson/<int:lesson_id>/', tutor_views.lesson_edit_page, name='lesson_edit_page'),
    path('delete_lesson/<int:lesson_id>/', tutor_views.delete_lesson, name='delete_lesson'),


    path('course_schedule_class/', tutor_views.course_schedule_class, name='course_schedule_class'),
    path('upcoming-classes/', tutor_views.upcoming_classes, name='upcoming_classes'),
    path('tutor/schedule-class/<int:course_id>/', tutor_views.tutor_schedule_class, name='tutor_schedule_class'),
    path('view-scheduled-classes/', tutor_views.view_scheduled_classes, name='view_scheduled_classes'),
    path('delete-class-schedule/<int:class_schedule_id>/', tutor_views.delete_class_schedule, name='delete_class_schedule'),

    path('tutor-courses/', tutor_views.tutor_courses, name='tutor_courses'),
    path('view-course-sessions/<int:course_id>/', tutor_views.view_course_sessions, name='view_course_sessions'),
    path('take-attendance/<int:session_id>/', tutor_views.take_attendance, name='take_attendance'),

    path('quiz_form/<int:course_id>/', tutor_views.quiz_form, name='quiz_form'),
    path('update_question_status/<int:question_id>/', tutor_views.update_question_status, name='update_question_status'),







    # path("staff/get_students/", staff_views.get_ students, name='get_students'),
    # path("staff/attendance/fetch/", staff_views.get_student_attendance,
    #      name='get_student_attendance'),
    # path("staff/attendance/save/",
    #      staff_views.save_attendance, name='save_attendance'),
   
    # path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    
    
    # path('staff/result/fetch/', staff_views.fetch_student_result,
    #      name='fetch_student_result'),


    # <<<<<<<<<<<<<<admin vewss>>>>>>>>>>>>>>>

     path("admin_dashboard/home/", hod_views.admin_home, name='admin_home'),
     path("admin_view_profile", hod_views.admin_view_profile,name='admin_view_profile'),
     path('edit_admin_profile/', hod_views.edit_admin_profile, name='edit_admin_profile'),
     path("student/manage/", hod_views.manage_student, name='manage_student'),
     path('delete_student/<int:student_id>/', hod_views.delete_student, name='delete_student'),
     path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
     path('edit_tutor/<int:tutor_id>/', hod_views.edit_tutor, name='edit_tutor'),
     path("tutor/delete/<int:tutor_id>", hod_views.delete_tutor, name='delete_tutor'),
     path('pending-tutors/', PendingTutorListView.as_view(), name='pending_tutors'),
     path('approve-tutor/<int:tutor_id>/', approve_tutor, name='approve_tutor'),

    
     
     path("view_catgories", hod_views.view_catgories, name='view_catgories'),

     path('courses/<str:category_name>/', hod_views.filtered_course_list, name='filtered_course_list'),
     path('manage_tutor_courses', hod_views.manage_tutor_courses, name='manage_tutor_courses'),
#       path('activate-course/<int:course_id>/', hod_views.admin_toggle_course, {'action': 'activate'}, name='admin_activate_course'),

#     path('deactivate-course/<int:course_id>/', hod_views.admin_toggle_course, {'action': 'deactivate'}, name='admin_deactivate_course'),



     path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
     path('add_tutor/', hod_views.add_tutor, name='add_tutor'),
     path('student/edit/<int:student_id>', hod_views.edit_student, name='edit_student'),
     path("student/delete/<int:student_id>", hod_views.delete_student, name='delete_student'),
   
     path('reject_and_delete_tutor/<int:tutor_id>/', hod_views.reject_and_delete_tutor, name='reject_and_delete_tutor'),
     # path("admin/home/course/", hod_views.add_course, name='add_course'),
#     path("send_student_notification/", hod_views.send_student_notification,
#          name='send_student_notification'),
#     path("send_staff_notification/", hod_views.send_staff_notification,
#          name='send_staff_notification'),
#     path("add_session/", hod_views.add_session, name='add_session'),
#     path("admin_notify_student", hod_views.admin_notify_student,
#          name='admin_notify_student'),
#     
#     
#     path("check_email_availability", hod_views.check_email_availability,
#          name="check_email_availability"),
#     path("session/manage/", hod_views.manage_session, name='manage_session'),
#     path("session/edit/<int:session_id>",
#          hod_views.edit_session, name='edit_session'),
#     path("student/view/feedback/", hod_views.student_feedback_message,
#          name="student_feedback_message",),
#     path("staff/view/feedback/", hod_views.staff_feedback_message,
#          name="staff_feedback_message",),
#     path("student/view/leave/", hod_views.view_student_leave,
#          name="view_student_leave",),
#     path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
#     path("attendance/view/", hod_views.admin_view_attendance,
#          name="admin_view_attendance",),
#     path("attendance/fetch/", hod_views.get_admin_attendance,
#          name='get_admin_attendance'),
#     path("student/add/", hod_views.add_student, name='add_student'),
#     path("subject/add/", hod_views.add_subject, name='add_subject'),
#     path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
#     
#     
#     
#     
#     path("staff/delete/<int:staff_id>",
#          hod_views.delete_staff, name='delete_staff'),

#     path("course/delete/<int:course_id>",
#          hod_views.delete_course, name='delete_course'),

#     path("subject/delete/<int:subject_id>",
#          hod_views.delete_subject, name='delete_subject'),

#     path("session/delete/<int:session_id>",
#          hod_views.delete_session, name='delete_session'),

#     
    
#     path("course/edit/<int:course_id>",
#          hod_views.edit_course, name='edit_course'),
#     path("subject/edit/<int:subject_id>",
#          hod_views.edit_subject, name='edit_subject'),

]
