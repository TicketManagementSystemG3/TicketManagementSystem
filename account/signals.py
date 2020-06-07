from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from account.models import User


@receiver(post_save,sender=User)
def set_user_group(sender,instance,created,*args,**kwargs):

    if created:
        user = Group.objects.get(name="user")
        instance.groups.add(user)

        if instance.role == "AD":
            Admin = Group.objects.get(name = 'Admin')
            instance.groups.add(Admin)
            instance.send_welcome_mail()

        if instance.role == 'AG':
            Agent = Group.objects.get(name='Agent')
            instance.groups.add(Agent)
            
        
