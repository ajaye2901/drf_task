from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators

class UserRegistrationSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(style={"input_type" : "password"})

    class Meta:
        model = User
        fields = ["username","password","email","mobile"]

        def validate_password(self, data) :
            validators.validate_password(password=data, user=User)
            return data