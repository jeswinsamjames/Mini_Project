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
   
    name = models.CharField(max_length=120,unique=True)
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
    LEVEL_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    GENRE_CHOICES = [
        ('Classical', 'Classical'),
        ('Jazz', 'Jazz'),
        ('Rock', 'Rock'),
        ('Pop', 'Pop'),
        # Add other genre choices as needed
    ]

    name = models.CharField(max_length=120, default='DefaultName')
    course = models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    tutor_name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Basic')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=True, null=True)
    description = models.TextField()
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, default=0.00)  # Allow null values and set default to 0
    is_active = models.BooleanField(default=True)
    enrolled_learners = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

   

    def update_sentiment_score(self):
        print("asds")
        reviews=RatingReview.objects.filter(course=self)
        print(121)
        total_sentiment_score = sum(review.sentiment_score for review in reviews)
        num_reviews = reviews.count()
        if num_reviews > 0:
            self.sentiment_score = total_sentiment_score / num_reviews
        else:
            self.sentiment_score = 0.00
        self.save()


 
    
    def experience_category(self):
        if self.years_of_experience <= 5:
            return '0-5 years'
        elif 5 < self.years_of_experience <= 10:
            return '5-10 years'
        elif 10 < self.years_of_experience <= 15:
            return '10-15 years'
        else:
            return '15+ years'

    def budget_category(self):
        if self.amount <= 500:
            return 'Limited budget'
        elif 500 < self.amount <= 1000:
            return 'Moderate budget'
        elif 1000 < self.amount <= 2000:
            return 'High budget'
        else:
            return 'No budget constraints'

    def str(self):
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
        
      
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)
  
class Attendance(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    is_present = models.BooleanField(null=True)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)  # Add the course field

    def __str__(self):
        return f"{self.learner.username} - {self.class_schedule.course.name} "
    
class Progress(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)

    lesson_material = models.ForeignKey('LessonMaterial', on_delete=models.CASCADE, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.learner.username} - {self.course_detail.name} - Module {self.module.module_number} - {self.lesson_material.title if self.lesson_material else 'Overall'}"
    
class Question(models.Model):
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Add this field
    unlock_condition = models.ForeignKey(Progress, on_delete=models.SET_NULL, blank=True, null=True)

    

    def __str__(self):
        return self.title

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)
    score = models.IntegerField(default=False)

    def save(self, *args, **kwargs):
        # Automatically set the score based on correctness of the response
        self.score = self.option.is_correct
        super(Response, self).save(*args, **kwargs) 



class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    # Add any other fields you need for the certificate

    def str(self):
        return f"Certificate for {self.user.username} - {self.course.course_title}"

# def calculate_sentiment_score(text):
#     # Your sentiment analysis code using NLTK or any other library
#     # Return sentiment score
#     pass

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.db import models
from django.contrib.auth.models import User
from .models import CourseDetail

class RatingReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate sentiment score and save it
        self.sentiment_score = self.calculate_sentiment_score(self.review)
        super().save(*args, **kwargs)
        self.course.update_sentiment_score()  # Update sentiment score of the associated course


    def calculate_sentiment_score(self, text):
        # Initialize NLTK's VADER sentiment analyzer
        sid = SentimentIntensityAnalyzer()
        # Calculate sentiment score
        sentiment_score = sid.polarity_scores(text)['compound']
        return sentiment_score
    
    def calculate_sentiment_score(self, text):
        # Initialize NLTK's VADER sentiment analyzer
        sid = SentimentIntensityAnalyzer()
        # Calculate sentiment score
        sentiment_score = sid.polarity_scores(text)['compound']
        return sentiment_score

    def str(self):
        return f"Rating: {self.rating}, Review: {self.review}"

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)

    
class Assignments(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_assignments')
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Changed field name
    due_date = models.DateTimeField()
    start_date = models.DateTimeField()  
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('mp3', 'MP3'),
        ('mp4', 'MP4'),
    )
    allowed_file_type = models.CharField(max_length=3, choices=FILE_TYPE_CHOICES)


    def __str__(self):
        return self.title
    
class UploadAssignment(models.Model):  # Changed model name to follow Python naming conventions
    feedback = models.TextField()
    files = models.FileField(upload_to='assignments/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_assignments')
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Changed field name
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)

    def __str__(self):
        return self.feedback



