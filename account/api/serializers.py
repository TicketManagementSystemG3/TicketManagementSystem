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
    
    
     
class EnableOrDisableUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk","username","email","phone","image","role","status"]
        read_only_fields = ["pk","username","email","phone","image","role"]

class PasswordChangeSerializer(serializers.Serializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self,data):

        password = data["password"]
        password2 = data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        
        return data

    # class Meta:
    #     model = User
    #     fields = ['password','password2']
    
    # def save(self):
    #     print(self.__dict__)
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']
    #     user = User.objects.get(username = self.request.get_username)

    #     if password != password2:

    #         raise serializers.ValidationError({"password": "Passwords must match."})

    #     user.set_password(password)
    #     user.save()
    #     return user





