from django import forms
from account.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):

    class Meta:

        model = User
        fields = ("username","email","password1","password2")

       
class CreateUserForm(UserCreationForm):
   
    def __init__(self, *args, **kwargs):
       super(CreateUserForm, self).__init__(*args, **kwargs)
       self.fields['password1'].required = False
       self.fields['password2'].required = False
       self.fields['password1'].widget.attrs['autocomplete'] = 'off'
       self.fields['password2'].widget.attrs['autocomplete'] = 'off'
       self.fields['password1'].widget = forms.HiddenInput()
       self.fields['password2'].widget = forms.HiddenInput()

    class Meta:

        model = User
        fields = ["email","role"]

        