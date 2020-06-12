from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import CreateView
from account.models import User
from account.forms import SignupForm
from account.forms import CreateUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from tms.utils import extract_username,generate_password
from django.contrib import messages

# Create your views here.

class SignupView(CreateView):

    form_class = SignupForm
    template_name = "account/signup.html"
    success_url = "index"
    

def index(request,*args,**kwargs):
    return render(request,"account/base.html")


class CreateUserView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    
    login_url = "login"
    permission_required = 'account.add_user'
    form_class = CreateUserForm
    template_name = "account/create_user.html"
    success_url = "create_user"

    def post(self,request,*args,**kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = extract_username(request.POST['email'])
            password = generate_password()
            user = User(username=username,email=request.POST["email"],role=request.POST['role'])
            user.set_password(password)
            user.save()
            user.send_login_mail(password)
            messages.success(request, f'new user has been created')
            return redirect("create_user")
        else:
            return render(request, "account/create_user.html", {'form': form})
       
    


