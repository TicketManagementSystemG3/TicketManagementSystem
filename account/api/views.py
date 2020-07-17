from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.api.serializers import ( SignUpSerializer,
                                      UserCreationSerializer,
                                      ProfileSerializer,
                                      EnableOrDisableUserSerializer,
                                      PasswordChangeSerializer,
                                      )
from account.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from account.api.permissions import IsProfilePermission
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions


class SignupApiView(APIView):
    
    def post(self,request,*args,**kwargs):
        
        userobj = SignUpSerializer(data=request.data)
        data = {}
        if userobj.is_valid():

            user = userobj.save()
            data["message"] = "user successfully created"
            data["email"] = user.email
            data["username"] = user.username 
            data["token"] = Token.objects.get(user=user).key
            return Response({"user":data},status= status.HTTP_201_CREATED)

        else:

            return Response(userobj.errors,status = status.HTTP_400_BAD_REQUEST)


class UserCreationView(APIView):
    queryset = User.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

    def post(self,request,*args,**kwargs):

        user_obj = UserCreationSerializer(data=request.data)
        data = {}
        if user_obj.is_valid():
            user = user_obj.save()
            data["message"] = "user creation is successfull"
            data["email"] = user.email
            data["user name"] = user.username
            return Response({"user":data},status= status.HTTP_201_CREATED)
        else:
            return Response(user_obj.errors,status = status.HTTP_400_BAD_REQUEST)


            

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsProfilePermission]

    def get(self,request,*args,**kwargs):
        try:
            profile_obj = User.objects.get(pk=self.kwargs['pk'])
        except:
            return Response({"error":"Invalid profile"},status = status.HTTP_400_BAD_REQUEST )

        self.check_object_permissions(self.request, profile_obj)
        prof_serialize = ProfileSerializer(profile_obj)
        return Response(prof_serialize.data)
    
    def put(self,request,*args,**kwargs):

        try:
            profile_obj = User.objects.get(pk=self.kwargs['pk'])
        except:
            return Response({"error":"Invalid profile"},status = status.HTTP_400_BAD_REQUEST )

        self.check_object_permissions(self.request, profile_obj)
        serializer = ProfileSerializer(profile_obj,data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['sucess']="profile successfully updated"
            return Response(data,status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class EnableDisableUserView(APIView):
    queryset = User.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

    def get(self,request,*args,**kwargs):

        try:
            users = User.objects.filter(status=self.kwargs['slug'])
        except:
            return Response({"error":"No Active users"},status = status.HTTP_400_BAD_REQUEST )
        serializer = EnableOrDisableUserSerializer(users,many=True)
        return Response({"users":serializer.data})
    
    def put(self,request,*args,**kwargs):
        print(self.kwargs)
        try:
            user = User.objects.get(pk=self.kwargs['pk'])
        except:
            return Response({"error":"Invalid user"},status = status.HTTP_400_BAD_REQUEST )
        
        dserializer = EnableOrDisableUserSerializer(user,data=request.data)
        data = {}
        if dserializer.is_valid():
            obj = dserializer.save()
            if obj.status == "DS":
                data["success"] = "User has been disabled successfully"
            else:
                data["success"] = "user has been enabled successfully"
            return Response(data,status= status.HTTP_201_CREATED)
        else:
            return Response(dserializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
class PasswordChangeView(APIView):
    queryset = User.objects.none()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]

    def post(self,request,*args,**kwargs):

        deserializer = PasswordChangeSerializer(data = request.data)
        data = {}
        if deserializer.is_valid():
            self.request.user.set_password(deserializer.validated_data['password'])
            self.request.user.save()
            data["success"] = "password changed successfully"
            return Response(data,status= status.HTTP_201_CREATED)
        else:
            return Response(deserializer.errors,status = status.HTTP_400_BAD_REQUEST)









       
