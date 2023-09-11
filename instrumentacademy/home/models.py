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
    teaching_experience = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Define the upload path

    def __str__(self):
        return self.user.username
    

class Course(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    instrument_name = models.CharField(max_length=100)
    description = models.TextField()
    # tutors = models.ManyToManyField(Tutor)
    # enrollments = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



  


    
# from ckeditor.fields import RichTextField

# class video(models.Model):
#     title = models.CharField(max_length=100, null=False)
#     # post = post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
#     serial_number = models.IntegerField(null=False)
#     video_id = models.CharField(max_length=100)
#     is_preview = models.BooleanField(default=False)
#     # desc = RichTextField(blank=True, null=True)

#     def __str__(self):
#         return self.title


#student profile

# class Student(models.Model):
#     admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
#     session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)

#     def __str__(self):
#         return self.admin.last_name + ", " + self.admin.first_name