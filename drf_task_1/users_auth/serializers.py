from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(style={"input_type" : "password"})


    def validate_password(self, data) :
        validators.validate_password(password=data, user=User)
        return data
    
    class Meta:
        model = User
        fields = ["username","password","email","mobile"]

        
class UserListSerializer(serializers.ModelSerializer) :
        
    def get_username(self, instance) :
        if instance.username:
            data = f"{instance.username}"
        return data

    class Meta:
        model = User
        fields = ["username","password","email","mobile","role_id","user_id"]

class LoginSerializer(serializers.ModelSerializer) :
        username = serializers.CharField(max_length=100)
        password = serializers.CharField(style={"input_type":"password"})

        class Meta:
            model = User
            fields = ["username","password"]

class LoginResponseSerializer(serializers.ModelSerializer) :
        access_token = serializers.SerializerMethodField()
        refresh_token = serializers.SerializerMethodField()

        
        def get_refresh_token(self, instance) :
            return str(RefreshToken.for_user(instance))
        
        def get_access_token(self, instance) :
            return str(RefreshToken.for_user(instance).access_token)
        
        class Meta:
            model = User
            fields = ["username","email","mobile","role_id","access_token","refresh_token"]

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)
 
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "mobile_phone",
            "status",
            "role",
        ]