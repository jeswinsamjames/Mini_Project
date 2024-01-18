from django.contrib import admin

from .models import *
from payment.models import *



def approve_as_tutor(modeladmin, request, queryset):
    # Update the isTutor value to 2 for selected users
    queryset.update(isTutor=2)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'isTutor')
    list_filter = ( 
        ('isTutor', admin.AllValuesFieldListFilter),
    )
    list_filter_title = 'Filter by User Type'
    actions = [approve_as_tutor]
    approve_as_tutor.short_description = "Approve selected users as tutors"




@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'instrument_name')
    
admin.site.register(Courses)
admin.site.register(CourseDetail)
admin.site.register(Enrollment)
admin.site.register(Module)
admin.site.register(LessonMaterial)
admin.site.register(ClassSchedule)
admin.site.register(Attendance)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Progress)




