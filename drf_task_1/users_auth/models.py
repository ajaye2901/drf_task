from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class Role(models.Model):
    ACTIVE = 0
    INACTIVE = 1
    
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")       
    )

    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=ACTIVE)

class User(AbstractUser) :
    ACTIVE = 0
    INACTIVE  = 1
    STATUS_CHOICE = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")
    )

    mobileno_errors = {
        "required" : "Mobile no required",
        "invalid" : "Enter a valid 10 digit no"
    }
    mobileno_validator = RegexValidator(
        regex = r"^\d{10}$", message = "Phoneno must be 10 digits without + or spaces."
    )
    email_errors = {
        "required" : "Email is required",
        "invalid" : "Enter a valid Email"
    }
    email_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", message="Email must be valid"
    )
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(
        "Email",
        max_length=50,
        validators=[email_validator],
        blank=False,
        null=False,
        unique=True,
        error_messages=email_errors
    )
    mobile = models.CharField(
        "Mobile Number",
        max_length=10,
        validators=[mobileno_validator],
        blank=False,
        null=False,
        unique=True,
        error_messages=mobileno_errors
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, default=0)
    role_id = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )