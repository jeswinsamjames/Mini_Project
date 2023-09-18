from django.urls import path,include
from . import views,student_views,tutor_views,hod_views
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static
from .hod_views import PendingTutorListView, approve_tutor
urlpatterns = [
    
    path('', views.index),
    
    path('leanerindex', views.leanerindex,name='learnerindex'),
   
    path('login', views.login,name='login'),
    
   
   
    
  
    path('homecontent', views.homecontent,name='homecontent'),
    path('index1', views.index1,name='index1'),
    path('mylearning', views.mylearning,name='mylearning'),


    path('logout', views.loggout,name='logout'),
    path('base', views.base),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('registration', views.registration,name="registration"),
    
    
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
   

 #<<<<<<<<<<<<<<Student>>>>>>>>>>>>>>>
    
    path("logout_user/", views.logout_user, name='user_logout'),
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance, name='student_view_attendance'),
    path("student/feedback/", student_views.student_feedback, name='student_feedback'),
#     path("student/fcmtoken/", student_views.student_fcmtoken,name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification, name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,name='student_view_result'),
    path('view_profile/learner/', student_views.view_profile_learner, name='view_profile_learner'),
    path('edit_profile/learner/', student_views.edit_profile_learner, name='edit_profile_learner'),

    #<<<<<<<<<<<<<<staff>>>>>>>>>>>>>>>

    path("tutor/home/", tutor_views.tutor_home, name='tutor_home'),
    path("tutor/view/profile/", tutor_views.tutor_view_profile,
         name='tutor_view_profile'),
    path("tutor/result/add/", tutor_views.tutor_add_result, name='tutor_add_result'),
    path("tutor/result/edit/", tutor_views.EditResultView,name='edit_student_result'),
    path("tutor/attendance/take/", tutor_views.tutor_take_attendance,
         name='tutor_take_attendance'),
    path("tutor/attendance/update/", tutor_views.tutor_update_attendance,
         name='tutor_update_attendance'),
    # path("tutor/attendance/update/",
    #      tutor_views.update_attendance, name='update_attendance'),
    path("tutor/view/notification/", tutor_views.tutor_view_notification,
         name="tutor_view_notification"),
    path("tutor/feedback/", tutor_views.tutor_feedback, name='tutor_feedback'),
    path('edit_profile/tutor/', tutor_views.edit_profile_tutor, name='edit_profile_tutor'),
    path('view_profile/tutor/', tutor_views.view_profile_tutor, name='view_profile_tutor'),
     path('create-course/', tutor_views.create_course, name='create_course'),
    path('course-list/', tutor_views.course_list, name='course_list'),
    path('manage-courses/', tutor_views.manage_courses, name='manage_courses'),
      path('edit-course/<int:course_id>/', tutor_views.edit_course, name='edit_course'),

    # Define the URL for the delete_course view with a dynamic course_id parameter
    path('delete-course/<int:course_id>/', tutor_views.delete_course, name='delete_course'),
   
   
    
    # path("staff/get_students/", staff_views.get_students, name='get_students'),
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
     path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
     path('edit_tutor/<int:tutor_id>/', hod_views.edit_tutor, name='edit_tutor'),
     path("tutor/delete/<int:tutor_id>", hod_views.delete_tutor, name='delete_tutor'),
     path('pending-tutors/', PendingTutorListView.as_view(), name='pending_tutors'),
     path('approve-tutor/<int:tutor_id>/', approve_tutor, name='approve_tutor'),

    
     path("admin/home/category/", hod_views.manage_course, name='manage_course'),
     path("view_catgories", hod_views.view_catgories, name='view_catgories'),
     path('courses/<str:category_name>/', hod_views.filtered_course_list, name='filtered_course_list'),
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
