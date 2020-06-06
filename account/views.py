from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import CreateView
from account.models import User
from account.forms import SignupForm

# Create your views here.
class SignupView(CreateView):

    model = User
    form_class = SignupForm
    template_name = "account/signup.html"
    success_url = "index"
    

def index(request,*args,**kwargs):
    return render(request,"account/base.html")