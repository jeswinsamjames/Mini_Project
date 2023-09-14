
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User  # Use the User model
        fields = ('first_name', 'last_name', 'email') # Fields to edit
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'address','specialist', 'description','phoneNo']


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