from django.urls import path,include
from home import views
urlpatterns = [
    
    path('', views.index),
    path('blog', views.blog),
    path('sample', views.sample),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    path('google_logout', views.google_logout,name='google_logout'),
    path('register', views.register, name="register"),
    path('base', views.base),
    path('forget', views.forget)


    
]
