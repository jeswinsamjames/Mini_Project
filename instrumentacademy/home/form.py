
# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from captcha.fields import ReCaptchaField
# class RegistrationForm(forms.Form):
#     full_name = forms.CharField(max_length=100, label='Full Name')
#     email = forms.EmailField(label='Email')
#     # phone_number = forms.CharField(max_length=10, label='Phone Number')
#     password = forms.CharField(widget=forms.PasswordInput(), label='Password')
#     confirmpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
#     captcha = ReCaptchaField()

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("This email address is already in use.")
#         return email
    
#     def clean_confirm_password(self):
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#         if password and confirm_password and password != confirm_password:
#             raise ValidationError("Passwords do not match.")
#         return confirm_password
    
