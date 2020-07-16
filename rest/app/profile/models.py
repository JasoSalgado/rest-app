import uuid
from django.db import models
from rest.app.user.models import User

class UserProfile(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = True)
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    first_name = models.CharField(max_length = 50, unique = False)
    last_name = models.CharField(max_length = 50, unique = False)
    phone_number = models.CharField(max_length = 10, unique = True, null = False, blank = False)
    host = models.BooleanField(default = True)
    
    class Meta:
        """
        To set table name in database
        """
        db_table = 'profile'