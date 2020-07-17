from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from account.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save,sender=User)
def set_user_group(sender,instance,created,*args,**kwargs):

    if created:
        user = Group.objects.get(name="user")
        instance.groups.add(user)
        Token.objects.create(user=instance)

        if instance.role == "AD":
            Admin = Group.objects.get(name = 'Admin')
            instance.groups.add(Admin)
            instance.send_welcome_mail()

        if instance.role == 'AG':
            Agent = Group.objects.get(name='Agent')
            instance.groups.add(Agent)
            
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    url = "http://127.0.0.1:8000/api"
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(url+reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('account/user_reset_password.html', context)
    email_plaintext_message = render_to_string('account/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Ticket Management System"),
        # message:
        email_plaintext_message,
        # from:
        'Dont Reply <do_not_reply@domain.com>',
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()      
