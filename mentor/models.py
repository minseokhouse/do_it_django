from django.contrib.auth.models import UserManager
from django.db import models
from user.models import User

# Create your models here.
from user.models import User


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('user.User', on_delete=models.CASCADE, default='')
    mentor = models.CharField(max_length=30)
    mentor_img = models.ImageField(upload_to='images/')
    mento_title = models.CharField(max_length=100)
    mento_content = models.CharField(max_length=5000)
    mento_type = models.CharField(max_length=50)

    def __str__(self):
        return self.email

