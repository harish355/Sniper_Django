import re
from django.http import JsonResponse
from rest_framework import permissions
from .models import Api_table
from .serializers import Api_data_Serializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .Zebul_api_funcs import *

class API_Data(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)
        try:
            userid=request.data['userid']
            api_key=request.data['api_key']
        except:
            return Response({"Message":"Invalid Data","Status":"400"}, status=status.HTTP_201_CREATED)
        if(len(list(Api_table.objects.filter(User=request.user)))==0): 

            if("Please generate API key" not in  str(get_encryption_key(get_user(userid,api_key)) )):
                obj=Api_table(userid=userid,api_key=api_key,User=request.user)
                obj.save()  
                return Response({
                "Message":"Api Key added",
                "Status":"200"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                "Message":"Enter A valid APi Key",
                "Status":"400"
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                    "Message":"Api Details already present"
                }, status=status.HTTP_201_CREATED)
        
    def get(self, request):
        try:
            api_obj=Api_table.objects.get(User=request.user)
            return Response({
                "Status":"200",
                "userid":api_obj.userid,
                "IsValid":"Yes"
            }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                "Message":"Add Api Details in User Settings"
            }, status=status.HTTP_400_BAD_REQUEST)


class API_update(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            userid=request.data['userid']
            api_key=request.data['api_key']
        except:
            return Response({"Message":"Invalid Data","Status":"400"}, status=status.HTTP_201_CREATED)
        if(len(list(Api_table.objects.filter(User=request.user)))==1):
            if("Please generate API key" not in  str(get_encryption_key(get_user(userid,api_key)) )):
               obj=Api_table.objects.get(User=request.user)
               obj.userid=userid
               obj.api_key=api_key
               obj.save()
               return Response({
                    "Message":"Api Key Updated",
                    "Status":"200"
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                "Message":"Enter A valid APi Key",
                "Status":"400"
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "Message":"No APi Data Found",
                "Status":"400"
                }, status=status.HTTP_201_CREATED)

class User_Api_SessionId(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            api_obj=Api_table.objects.get(User=request.user)
            user=get_user(api_obj.userid,api_obj.api_key)
            Session_id=user.getEncryptionKey()['sessionID']
            return Response({
                "Status":"200",
                "Session":str(Session_id)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "Message":str(e)
            }, status=status.HTTP_400_BAD_REQUEST)