from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from datetime import date
from dateutil.relativedelta import relativedelta
import re


class ContactForm(forms.Form):
    name=forms.CharField(max_length=50)
    email=forms.EmailField()
    subject=forms.CharField()
    message=forms.CharField()
    def clean(self) -> dict[str, Any]:
        return super().clean()
    

class Registration(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect,
        }

    avatar = forms.ImageField(required=True)
    hobbies = forms.MultipleChoiceField(
        choices=[('Reading', 'Reading'), ('Sports', 'Sports'), ('Music', 'Music')],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    # Validation for first name
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if not fname.isalpha():
            raise forms.ValidationError("First Name should only contain alphabetic characters.")
        return fname

    # Validation for last name
    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if not lname.isalpha():
            raise forms.ValidationError("Last Name should only contain alphabetic characters.")
        return lname

    # Validation for phone number
    def clean_phn(self):
        phn = self.cleaned_data.get('phn')
        if not re.match(r'^\d{10,15}$', phn):
            raise forms.ValidationError("Phone number must be between 10 and 15 digits and contain only digits.")
        return phn

    # Validation for email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "@example.com" in email:  # Example of restricted domain
            raise forms.ValidationError("Emails from 'example.com' are not allowed.")
        return email

    # Validation for date of birth (minimum age 18)
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            age = relativedelta(date.today(), dob).years
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old.")
        return dob

    # Validation for hobbies
    def clean_hobbies(self):
        hobbies = self.cleaned_data.get('hobbies')
        if not hobbies:
            raise forms.ValidationError("You must select at least one hobby.")
        if len(hobbies) > 3:
            raise forms.ValidationError("You can select a maximum of 3 hobbies.")
        return hobbies

    # Validation for avatar size
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar.size > 2 * 1024 * 1024:  # 2 MB limit
            raise forms.ValidationError("Avatar file size cannot exceed 2MB.")
        return avatar

    # Overall form validation (country and state validation)
    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        state = cleaned_data.get('state')

        valid_states_by_country = {
            'India': ['Kerala', 'TamilNadu', 'Karnataka'],
            'USA': ['California', 'Texas', 'Florida'],
            'UK': ['England', 'Scotland', 'Wales'],
        }

        if country and state:
            if state not in valid_states_by_country.get(country, []):
                self.add_error('state', f"{state} is not a valid state for {country}.")
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    keep_logged_in = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Keep me logged in")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email")


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # You can add more fields if needed


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student  # The model that the form is related to (e.g., Profile model)
        fields = '__all__'  # List of fields you want to include in the form

    # Custom validations if needed
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if Student.objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email
    
    def clean_phn(self):
        phn = self.cleaned_data.get('phn')
        if len(phn) < 10 or len(phn) > 15:
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phn
