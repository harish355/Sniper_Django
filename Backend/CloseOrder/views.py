from django.http import JsonResponse
from .models import CloseOrders
from OpenOrder.serializers import OpenOrderSerializer, CloseOrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated


class CloseOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        CloseObj = CloseOrders.objects.filter(User=request.user)
        serialized_obj = CloseOrderSerializer(CloseObj, many=True)
        return Response(serialized_obj.data)


class Delete_Close_Order(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        id=request.data['id']
        close_obj=CloseOrders.objects.get(id=id)
        if(close_obj.User==request.user):
            close_obj.delete()

            Resp = {
                'Status': '200',
                'Message': 'Success'
            }
            return Response(Resp, status=status.HTTP_201_CREATED)
        return Response({
                'Status': '400',
                'Message': "Couldn't Delete"
        }, status=status.HTTP_400_BAD_REQUEST)


class Clear_All_CloseOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        close_obj=CloseOrders.objects.filter(User=request.user)
        try:
            for obj in close_obj:
                obj.delete()
            Resp = {
                    'Status': '200',
                    'Message': 'Success'
                }
            return Response(Resp, status=status.HTTP_201_CREATED)
        except:
            return Response({
                    'Status': '400',
                    'Message': "Couldn't Delete"
            }, status=status.HTTP_400_BAD_REQUEST)
