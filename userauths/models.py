from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True,null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self) -> str:
        return self.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
