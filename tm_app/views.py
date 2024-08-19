from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from .serializer import UserSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import Task

class RegisterApiView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user created"},status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
class LoginApiView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        data=request.data
        user = get_object_or_404(User,username=data['username'])
        if user.check_password(data['password']):
            token,created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({"token":token.key,"user":serializer.data},status=HTTP_200_OK)
        
class LogoutApiView(APIView):
    def post(self,request):
        user = Token.objects.get(user=request.user)
        user.delete()
        return Response({"Logout Successfully"},status=HTTP_200_OK)
       
class TaskApiView(APIView):
    def post(self,request):
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(username=request.user)
            return Response(serializer.data,status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        obj = Task.objects.filter(username=request.user)
        serializer = TaskSerializer(obj,many=True)
        return Response(serializer.data,status=HTTP_200_OK)
        
class TaskDetailApiView(APIView):
    def get_object(self,pk):
        try:
            return Task.objects.get(pk=pk,username=self.request.user)
        except Task.DoesNotExist:
            return Response({'Task not found'},status=HTTP_404_NOT_FOUND)
        
    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = TaskSerializer(obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        data = request.data
        # obj = Task.objects.get(pk=pk,username=request.user)
        obj = self.get_object(pk)
        serializer = TaskSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        data = request.data
        obj = self.get_object(pk)
        serializer = TaskSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response({"Task deleted"},status=HTTP_200_OK)
        
class TaskPriorityApiView(APIView):
    def get(self,request,pri):
        obj = Task.objects.filter(priority=pri,username=request.user)
        serializer = TaskSerializer(obj,many=True)
        if serializer.data == []:
            return Response({"Task Not Found"},status=HTTP_404_NOT_FOUND)
        return Response(serializer.data,status=HTTP_200_OK)

