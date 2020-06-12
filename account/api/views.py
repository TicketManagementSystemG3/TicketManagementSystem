from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.api.serializers import SignUpSerializer
from account.api.serializers import UserCreationSerializer
from account.api.serializers import ProfileSerializer
from account.models import User



class SignupApiView(APIView):
    
    def post(self,request,*args,**kwargs):
        
        userobj = SignUpSerializer(data=request.data)
        data = {}
        if userobj.is_valid():

            user = userobj.save()
            data['message'] = "user successfully created"
            data["email"] = user.email
            data["username"] = user.username
            return Response({"user":data},status= status.HTTP_201_CREATED)

        else:

            return Response(userobj.errors,status = status.HTTP_400_BAD_REQUEST)


class UserCreationView(APIView):

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

    def get(self,request,*args,**kwargs):
        try:
            profile_obj = User.objects.get(pk=self.kwargs['pk'])
        except:
            return Response({"error":"Invalid profile"},status = status.HTTP_400_BAD_REQUEST )
        prof_serialize = ProfileSerializer(profile_obj)
        return Response(prof_serialize.data)
    
    def put(self,request,*args,**kwargs):

        try:
            profile_obj = User.objects.get(pk=self.kwargs['pk'])
        except:
            return Response({"error":"Invalid profile"},status = status.HTTP_400_BAD_REQUEST )

        serializer = ProfileSerializer(profile_obj,data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['sucess']="profile successfully updated"
            return Response(data,status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)







            
#             cat_obj = Category.objects.get(id = cat_data.get('id'))
#         except:
#             return Response({"error":"Invalid category"},status = status.HTTP_400_BAD_REQUEST )







       
