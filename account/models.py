from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.mail import send_mail
from django.http import HttpResponse


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
        return self.username

    def make_admin(self):
        self.is_staff = True
        self.save()
    
    def send_welcome_mail(self):
        res = send_mail("hello "+self.username, "Welcome to TMS you are admin now.", 'Dont Reply <do_not_reply@domain.com>',[self.email])
        return HttpResponse('%s'%res)


