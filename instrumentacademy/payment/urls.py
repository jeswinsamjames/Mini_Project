
from django.contrib import admin
from django.urls import path
from payment import views
from django.urls import path
from . import views

app_name = 'payment'
 
urlpatterns = [
    path('homepage/<int:course_id>/', views.homepage, name='homepage'),
    path('paymenthandler/<int:course_id>/', views.paymenthandler, name='paymenthandler'),
    path('tutor/enrolled_learners/<int:course_id>/', views.learners_enrolled_through_payment, name='enrolled_learners'),

    path('admin/', admin.site.urls),

]