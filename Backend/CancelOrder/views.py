from django.http import JsonResponse
from .models import CanceledOrders
from OpenOrder.serializers import OpenOrderSerializer, CancelOrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated


class CancelOrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        CanceledObj = CanceledOrders.objects.filter(User=request.user)
        serialized_obj = CancelOrderSerializer(CanceledObj, many=True)
        return Response(serialized_obj.data)


class Delete_CancelOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            id=request.data['id']
            close_obj=CanceledOrders.objects.get(id=id)
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
        except Exception as e:
            return Response({
                'Status': '400',
                'Message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class Clear_All_CancelOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            close_obj=CanceledOrders.objects.filter(User=request.user)
            for obj in close_obj:
                obj.delete()
            Resp = {
                    'Status': '200',
                    'Message': 'Success'
            }
            return Response(Resp, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                    'Status': '400',
                    'Message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
