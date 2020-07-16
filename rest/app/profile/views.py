from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest.app.user.serializers import UserRegistrationSerializer
from rest.app.profile.models import UserProfile

"""
Using RetrieveAPIView as we want to retrieve a single instance.
Set permission_classes to IsAuthenticated, so the only user who is authenticated can hit this API and the authentication_class should be JWT
"""
class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user = request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success' : 'true',
                'status code' : status_code,
                'message' : 'User profile fetched successfully',
                'data' : [{
                    'first_name' : user_profile.first_name,
                    'last_name' : user_profile.last_name,
                    'phone_number' : user_profile.phone_number,
                    'host' : user_profile.host,
                }]
            }
        
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success' : 'false',
                'status code' : status.HTTP_400_BAD_REQUEST,
                'message' : 'User does not exist',
                'error' : str(e)
            }
        return Response(response, status = status_code)