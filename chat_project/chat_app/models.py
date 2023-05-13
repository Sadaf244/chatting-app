from django.db import models
from django.contrib.auth.models import AbstractUser
class Interest(models.Model):
    
    name = models.CharField(max_length=50,null=True, blank=True)
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Unnamed Object"

class ChatUser(AbstractUser):
    username = models.CharField(max_length=500, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(unique=True,null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True,null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
   
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    password = models.CharField(max_length=255,null=True, blank=True)
    is_active = models.BooleanField(default=False,null=True, blank=True)
    interests = models.ManyToManyField(Interest)
        
    COUNTRY="country"  
    INTEREST="interests"
    
    def __str__(self):
        if self.email:
            return self.email
        else:
            return "Unnamed Object"

class Connection(models.Model):
    user1 = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='connections_as_user1')
    user2 = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='connections_as_user2')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)