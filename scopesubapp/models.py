from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.
class ContactModel(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.TextField()
    message=models.TextField()

class Student(models.Model):
    # First Name
    fname = models.CharField(max_length=20)
    
    # Last Name
    lname = models.CharField(max_length=20)
    
    # Gender choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Date of Birth
    dob = models.DateField()
    
    # Email
    email = models.EmailField(unique=True)
    
    # Phone Number
    phn = models.CharField(max_length=15,unique=True)  # Length reduced to match phone number validation
    
    # Country
    country = models.CharField(max_length=30)
    
    # State
    state = models.CharField(max_length=30)
    
    # City
    city = models.CharField(max_length=20)
    
    # Hobbies (using Comma-Separated String)
    hobbies = models.CharField(max_length=100)  # Can hold multiple hobbies separated by commas
    
    # Avatar upload
    avatar = models.FileField(null=True, upload_to='mydocs')

    def __str__(self):
        return f"{self.fname} {self.lname}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, default="default_username")  # Add default
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings

# Profile model that extends the base User model
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')  # Reference to the CustomUser model
#     fname = models.CharField(max_length=100)  # First Name
#     lname = models.CharField(max_length=100)  # Last Name
#     gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])  # Gender choices
#     dob = models.DateField()  # Date of Birth
#     email = models.EmailField()  # Email address
#     phn = models.CharField(max_length=15)  # Phone number
#     country = models.CharField(max_length=100)  # Country
#     state = models.CharField(max_length=100)  # State
#     city = models.CharField(max_length=100)  # City
#     hobbies = models.TextField(blank=True)  # Hobbies (as text)
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Avatar image (optional)

#     def __str__(self):
#         return f"{self.fname} {self.lname}'s Profile"

#     # Optional: A method to return full name
#     def full_name(self):
#         return f"{self.fname} {self.lname}"
