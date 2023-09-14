from django.db import models
from django.contrib.auth.models import User
# Create your models here.


    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isTutor = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phoneNo = models.BigIntegerField(null=True, blank=True)
    specialist = models.CharField(max_length=50, choices=[('piano', 'Piano'), ('violin', 'Violin'), ('guitar', 'Guitar'), ('other', 'Other')], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    qualifications = models.CharField(max_length=255, blank=True, null=True)
    teaching_experience = models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Define the upload path
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    def __str__(self):
        return self.user.username
    

class category(models.Model): 
   
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    instrument_name = models.CharField(max_length=100)
    description = models.TextField()
  
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class Courses(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    course_type = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tutor.username}'s {self.course_type.name} Course"

class CourseDetail(models.Model):
    name = models.CharField(max_length=120, default='DefaultName')
    course = models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    tutor_name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.tutor_name}'s "

