from django.shortcuts import render
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserRegister(generics.CreateAPIView) :
    
    def get_serializer_class(self):
        return UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()  