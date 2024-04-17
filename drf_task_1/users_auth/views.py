from django.shortcuts import render
from .serializers import UserRegistrationSerializer, UserListSerializer, LoginSerializer, LoginResponseSerializer, UserCreateUpdateSerializer
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.db.models import Q
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.contrib.auth import authenticate


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

        
class Login(generics.ListAPIView) :
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    queryset = User.objects.none()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data  
            try:
                user_obj = User.objects.get(
                    Q(username__iexact=data["username"]) |
                    Q(email__iexact=data["username"])
                )
                print(user_obj.password)
                if (data['password'], user_obj.password):  
                    user_obj.last_login = timezone.now()
                    user_obj.save()
 
                    resp = LoginResponseSerializer(instance=user_obj)
                    return Response(resp.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Invalid credentials", "status": "1"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response({"message": "Invalid user", "status": "1"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserList(generics.ListAPIView) :
    permission_classes = [AllowAny]
    search_fields = ["username", "email", "user_id"]
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self) :
        return UserListSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        queryset = queryset.filter(status=0)
        return queryset.order_by("user_id")
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserGetById(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(status=0)
    lookup_field = "pk"
    serializer_class = UserListSerializer
 
    def get(self, request, pk, format=None):
        instance = self.get_object()
        serializer = UserListSerializer(instance)
        return Response(serializer.data)
   
 
    def put(self, request, pk, format=None):
        instance = self.get_object()
        serializer = UserCreateUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status':'0',
                    'message':"successfully updated",
                    'body':serializer.data,
                }
            )
        return Response(
            serializer.errors,
        )
   
    def delete(self, request, pk, format=None):
        details = self.get_object()
        try:
            details.status = 1
            details.save()
            return Response({"status":"0", "message":"user deleted"})
        except:
            return Response({"status":"1", "message":"deletion failed"})