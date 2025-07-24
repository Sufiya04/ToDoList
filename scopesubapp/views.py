from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.core.mail import send_mail,EmailMultiAlternatives
from django.http import HttpResponse,Http404
from django.conf import settings
from django.contrib.auth import login,authenticate,logout, update_session_auth_hash,get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import AnonymousUser

# Create your views here.
def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    form=ContactForm()
    return render(request,'contact.html',{'form':form})

def mailsend(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            n=form.cleaned_data['name']
            e=form.cleaned_data['email']
            s=form.cleaned_data['subject']
            m=form.cleaned_data['message']
            ContactModel.objects.create(name=n,email=e,subject=s,message=m).save()
            try:
                send_mail(s,m,settings.EMAIL_HOST_USER,[e],fail_silently=False)
                return HttpResponse("Email send Successfully.Thank You for Contacting Us!!")
            except Exception as e:
                print(f"Error Sending email:{e}")
                return HttpResponse("Unable to send an email right now")
        else:
            form=ContactForm()
            print("Invalid Form")
            print(form.errors)
            return render(request,'contact.html',{'form':form})
    else:
        form=ContactForm()
        print("Invalid Request")
        return render(request,'contact.html',{'form':form})
    
def register(request):
    if request.method == 'POST':
        form = Registration(request.POST, request.FILES)
        if form.is_valid():
            # Save form data
            student = form.save()  # `commit=False` to allow further customization
            
            # Process hobbies if needed
            student.hobbies = ', '.join(request.POST.getlist('hobbies'))  # Convert list to comma-separated string

            # student.save()  # Save the student instance after setting hobbies

            try:
                # Prepare and send the admin email
                sub1 = "New user registered"
                mes1 = render_to_string('adminmail.html', {
                    'f': student.fname,
                    'l': student.lname,
                    'e': student.email,
                    'p': student.phn,
                    'avatar_cid': 'avatar_image'
                })
                email1 = EmailMultiAlternatives(sub1, mes1, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                email1.content_subtype = 'html'

                # Attach logo image
                logo_path = finders.find('images/logo.png')
                if logo_path and os.path.exists(logo_path):
                    with open(logo_path, 'rb') as logo_file:
                        logo_image = MIMEImage(logo_file.read())
                        logo_image.add_header('Content-ID', '<logo_image>')
                        logo_image.add_header('Content-Disposition', 'inline', filename='logo.png')

                # Attach avatar image
                avatar_path = student.avatar.path
                with open(avatar_path, 'rb') as avatar_file:
                    avatar_image = MIMEImage(avatar_file.read())
                    avatar_image.add_header('Content-ID', '<avatar_image>')
                    avatar_image.add_header('Content-Disposition', 'inline', filename='avatar.png')

                # Attach both images to the admin email
                email1.attach(logo_image)
                email1.attach(avatar_image)
                email1.send()

                # Prepare and send the user email
                sub2 = "Registration successful"
                mes2 = render_to_string('usermail.html', {
                    'f': student.fname,
                    'l': student.lname,
                    'e': student.email,
                    'avatar_cid': 'avatar_image'
                })
                email2 = EmailMultiAlternatives(sub2, mes2, settings.EMAIL_HOST_USER, [student.email])
                email2.content_subtype = 'html'

                # Attach both images to the user email
                email2.attach(logo_image)
                email2.attach(avatar_image)
                email2.send()

                return render(request, 'regsub.html')
            except Exception as e:
                print(f"Error sending email: {e}")
                return HttpResponse("Unable to send an email right now.")
        else:
            # Re-render the form with validation errors
            print(form.errors)
            return render(request, 'reg.html', {'form': form})
    else:
        # GET request to render the empty registration form
        form = Registration()
        return render(request, 'reg.html', {'form': form})
    
def userlogin(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home') 
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid form data")
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})   

def signin(request):
    return render(request,'signin.html')

def course(request):
    return render(request,'course.html')

def profile(request):
    return render(request,'profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def generate_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            temp_password = get_random_string(8)  # Generate a random 8-character password
            user.set_password(temp_password)
            user.save()
            
            # Send an email with the temporary password
            send_mail(
                'Temporary Password',
                f'Your temporary password is {temp_password}',
                'admin@yourapp.com',
                [email],
                fail_silently=False,
            )
            return redirect('login')
        except CustomUser.DoesNotExist:
            return render(request, 'newpass.html', {'error': 'Email not found'})
    return render(request, 'newpass.html')

@login_required
def set_new_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            # Directly save the password without hashing
            user = request.user
            user.password = new_password  # This saves the password as plain text
            user.save()

            return redirect('dashboard')
        else:
            # Handle password mismatch
            return render(request, 'newpass.html', {'error': 'Passwords do not match.'})
    return render(request, 'newpass.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Handle the "Keep me logged in" checkbox
            if request.POST.get('keep_logged_in'):
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Close the session on browser close

            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def dashboard_view(request):
    if isinstance(request.user, AnonymousUser):
        # Handle the case where the user is not logged in (e.g., redirect to login page)
        return redirect('login') 
    # Example of setting and getting session data
    request.session['last_login_time'] = str(datetime.now())
    last_login = request.session.get('last_login_time', None)

    # Retrieve the logged-in user's student data (assuming email is unique)
    try:
        student = Student.objects.get(email=request.user.email)  # Ensure email matches the logged-in user
    except Student.DoesNotExist:
        student = None  # Handle case where student data does not exist

    # Pass student data to the template
    return render(request, 'dashboard.html', {
        'last_login': last_login,
        'student': student
    })

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user data
            login(request, user)  # Log the user in after sign-up
            return redirect('dashboard')  # Redirect to a dashboard page or any other page
        else:
            print(form.errors)  # Print errors if form is invalid
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def student_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(128600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SetNewPasswordForm

@login_required
def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')

            # Set the new password for the logged-in user
            request.user.set_password(new_password)
            request.user.save()

            # Important: Keep the user logged in after password change
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Your password has been successfully updated.')
            return redirect('dashboard')  # Redirect to a dashboard or any other page

    else:
        form = SetNewPasswordForm()

    return render(request, 'set_new_password.html', {'form': form})


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                temp_password = get_random_string(length=8)
                
                # Set the new password and save
                user.set_password(temp_password)
                user.save()
                
                # Send an email with the temporary password
                send_mail(
                    'Your Temporary Password',
                    f'Here is your temporary password: {temp_password}',
                    'admin@example.com',  # Update this to a valid "from" email
                    [email],
                    fail_silently=False,
                )
                
                # Optional: You can display a success message
                messages.success(request, 'A temporary password has been sent to your email.')
                
                # Redirect to the login page
                return redirect('login')
                
            except User.DoesNotExist:
                # Add an error if the email doesn't exist in the database
                form.add_error('email', 'No user found with this email address.')
    else:
        form = ResetPasswordForm()
        
    return render(request, 'reset_password.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'dashboard.html', {'form': form})


@login_required
def profile_view(request):
   
    # Example of setting and getting session data
    # request.session['last_login_time'] = str(datetime.now())
    # last_login = request.session.get('last_login_time', None)

    # Retrieve the logged-in user's student data (assuming email is unique)
    try:
        student = Student.objects.get(email=request.user.email)  # Ensure email matches the logged-in user
    except Student.DoesNotExist:
        student = None  # Handle case where student data does not exist

    # Pass student data to the template
    return render(request, 'dashboard.html', {
        # 'last_login': last_login,
        'student': student
    })

@login_required
def edit_profile(request):
    # Fetch the existing Student record for the logged-in user
    try:
        student = Student.objects.get(email=request.user.email)
    except Student.DoesNotExist:
        raise Http404("Student not found")
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # Ensure the user field is set
            student.save()
            return redirect('dashboard')  # Redirect after successful update
    else:
        form = ProfileForm(instance=student)  # Pre-fill the form

    return render(request, 'profile.html', {'form': form})