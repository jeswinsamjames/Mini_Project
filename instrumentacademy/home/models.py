from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    enrolled_learners = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')


    def __str__(self):
        return f"{self.name}"

class Enrollment(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.learner.username} enrolled in {self.course.name}"
    

class Module(models.Model):
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    module_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Module {self.module_number}: {self.title}"

class LessonMaterial(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE,related_name='courses',blank=True,null=True)  # Link the material to a specific course 
    module = models.ForeignKey(Module, on_delete=models.CASCADE,related_name='modules',blank=True,null=True)  # Link the material to a specific module
    description = models.TextField(blank=True, null=True)
    material_file = models.FileField(upload_to='lesson_materials/')
    created_at = models.DateTimeField(auto_now_add=True)
    material_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Material {self.material_number}: {self.title}"
    
class ClassSchedule(models.Model):
        
        course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
        start_datetime = models.DateTimeField()
        meeting_link = models.URLField()
        description = models.TextField(blank=True, null=True)
        duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)



        def __str__(self):
            return f"{self.course.name} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
      