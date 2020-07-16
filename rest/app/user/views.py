from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest.app.user.serializers import UserRegistrationSerializer, UserLoginSerializer

"""
It creates a view by extending CreateAPIView. The serializer_class tells which serializer to user and the permission_classes handles who can access the API
"""

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message' : 'User registered successfully',
        }
        
        return Response(response, status = status_code)

"""
It returns the token created for the user
"""
class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message' : 'User logged in successfully',
            'token' : serializer.data['token'],
        }
        status_code = status.HTTP_200_OK
        
        return Response(response, status = status_code)