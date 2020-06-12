from rest_framework import serializers
from account.models import User
from tms.utils import extract_username
from tms.utils import generate_password

class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']
    
    def	save(self):
        user = User(email=self.validated_data['email'],username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:

            raise serializers.ValidationError({"password": "Passwords must match."})

        user.set_password(password)
        user.save()
        return user

class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','role']
    
    def save(self):
        email=self.validated_data['email']    
        username = extract_username(email)
        password = generate_password()
        user = User(email=email,username=username,role=self.validated_data['role'])
        user.set_password(password)
        user.save()
        user.send_login_mail(password)
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","image","address","phone"]
    
    
     


