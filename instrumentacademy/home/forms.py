
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User  # Use the User model
        fields = ('first_name', 'last_name', 'email') # Fields to edit
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'address','specialist', 'description','phoneNo','profile_picture']
        # widgets = {
        #     'gender': forms.Select(attrs={'class': 'form-control'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'specialist': forms.TextInput(attrs={'class': 'form-control'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        #     'phoneNo': forms.TextInput(attrs={'class': 'form-control'}),
        #     'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        # }


class TutorForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            
            
            'gender',
            'address',
            'phoneNo',
            'specialist',
            'description',
            'profile_picture',
        )
        
    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False  # Make profile picture not required

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']



class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseDetail
        fields = [

            'name',
            'years_of_experience',
            'description',
            'image',
            'is_active',  # Include the is_active field in the form
        ]

        widgets = {
         'name': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'required'}),  # Add 'required' here
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'module_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'module_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LessonMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super(LessonMaterialForm, self).__init__(*args, **kwargs)
        
        if course_id:
            # Filter the modules based on the selected course
            self.fields['module'].queryset = Module.objects.filter(course_id=course_id)

    class Meta:
        model = LessonMaterial
        fields = ['title', 'module', 'description', 'material_file', 'material_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'material_file': forms.FileInput(attrs={'class': 'form-control'}),
            'material_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean_material_number(self):
        material_number = self.cleaned_data['material_number']
        if material_number < 0:
            raise ValidationError("Material number cannot be negative.")
        return material_number

    def clean_material_file(self):
        material_file = self.cleaned_data['material_file']
        if not material_file.name.endswith('.mp4'):
            raise ValidationError("Please upload a valid video file (MP4 format).")
        return material_file
