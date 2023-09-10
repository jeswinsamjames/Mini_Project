from django.contrib import admin

from .models import *




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




@admin.register(Course)
class CourseListAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'enrollments', 'created_at', 'updated_at')
    search_fields = ('name', 'title')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'title': ('name',)}

