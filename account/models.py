from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.mail import send_mail
from django.http import HttpResponse
from random import random,shuffle
import string
import re


# Create your models here.
class User(AbstractUser):
    role_type = [("AG","agent"),("AD","admin")]

    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=10,blank=True,choices=role_type,default="AD")
    image = models.ImageField(blank=True,default="default.jpg",upload_to="profile/")

    def save(self,*args,**kwargs):

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def __str__(self):
        return self.email

    def make_admin(self):
        self.is_staff = True
        self.save()
    
    def send_welcome_mail(self):

        sub = "hello "+self.username
        body = "Welcome to TMS you are admin now."
        from_mail = 'Dont Reply <do_not_reply@domain.com>'

        res = send_mail(sub,body,from_mail,[self.email])

        return HttpResponse('%s'%res)


    def send_login_mail(self,password):

        role = [roles[1] for roles in User.role_type if self.role == roles[0]]
        link = "http://127.0.0.1:8000/accounts/password_change/"
        sub = "hello "+self.username
        body = '''Welcome to TMS you are {} now.
                
                  Please login with the below user name and password.after logging in
                  please change the password.
                  username:{}
                  password:{}
                  please click on the below link to login
                  {}'''.format(role[0],self.username,password,link)
        from_mail = 'Dont Reply <do_not_reply@domain.com>'
        res = send_mail(sub,body,from_mail,[self.email])
        return HttpResponse('%s'%res)