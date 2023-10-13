from django.db import models
from django.contrib.auth.models import User
from home.models import CourseDetail

# Create your models here.
class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )
    items = models.ManyToManyField(CourseDetail)

    def __str__(self):
        course_names = ', '.join([course.name for course in self.items.all()])
        return f'Order {self.pk} - {self.user.username} - Courses: {course_names} '

    class Meta:
        verbose_name_plural = 'Orders'