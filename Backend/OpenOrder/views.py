from django.http import JsonResponse
from .models import OpenOrders
from .serializers import OpenOrderSerializer, CloseOrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .Zebul_api_funcs import *
from User_Settings.models import Api_table
from CancelOrder.models import CanceledOrders

class OpenOrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        OpenOrder = OpenOrders.objects.filter(User=request.user)
        serialized_obj = OpenOrderSerializer(OpenOrder, many=True)
        return Response(serialized_obj.data)

class Cancel_open_order(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            Order_Number=request.data['Order_Number']
        except:
            return Response({
                "Status":200,
                "Message":"Order Number data not present"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            open_obj=OpenOrders.objects.get(Order_Number=Order_Number)
            if("OPEN" in open_obj.Status.upper()):
                Api_object=Api_table.objects.get(User=request.user)
                User=get_user(Api_object.userid,Api_object.api_key)
                token=open_obj.Token_id

                Message=cancel_order(User,open_obj.Exchange,open_obj.Order_Number,token)
                print(Message)
                Message=dict(Message)
                if(Message['stat']=="ok" or Message['stat']=="Ok"):
                    open_obj.delete()
                    return Response({
                        "Status":200,
                        "Message":"Open Order Cancelled"
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "Status":200,
                        "Message":str(Message['emsg'])
                    }, status=status.HTTP_201_CREATED)
            return Response({
                        "Status":400,
                        "Message":"This is not an Open Order"
                    }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                        "Status":500,
                        "Message":str(e)
                    }, status=status.HTTP_201_CREATED)
        
class Square_Off(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            pCode=request.data['Order_type']
            Quantity=request.data['Quantity']
            Order_Number=request.data['Order_Number']
        except:
            return Response({
                    "Status":400,
                    "Message":"Order Type , Quantity and Order_Number data must be present"
                }, status=status.HTTP_201_CREATED)
        try:
            open_obj=OpenOrders.objects.get(Order_Number=Order_Number)
            if(open_obj.Status.upper()!="OPEN"):
                Api_object=Api_table.objects.get(User=request.user)
                User=get_user(Api_object.userid,Api_object.api_key)

                msg=squareoff_positions(user=User,exchange=open_obj.Exchange,symbol=open_obj.Chart_Symbol,
                qty=Quantity,pCode=pCode,
                tokenno=open_obj.Token_id)
                print(User,open_obj.Exchange,open_obj.Chart_Symbol,
                Quantity,pCode,
                open_obj.Token_id)
                return Response({
                        "Status":200,
                        "Message":str(msg)
                    }, status=status.HTTP_201_CREATED)
            return Response({
                        "Status":200,
                        "Message":"Open order is not Placed Yet"
                    }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                        "Status":500,
                        "Message":str(e)
                    }, status=status.HTTP_201_CREATED)


class Close_Open_Order(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            Order_Number=request.data['Order_Number']
        except:
            return Response({
                    "Status":400,
                    "Message":"Order_Number data must be present"
                }, status=status.HTTP_201_CREATED)
        try:
            open_obj=OpenOrders.objects.get(Order_Number=Order_Number)
            Api_object=Api_table.objects.get(User=request.user)
            User=get_user(Api_object.userid,Api_object.api_key)
            token=open_obj.Token_id
            msg=exitboorder(user=User,nestOrderNumber=Order_Number,symbolOrderId=token,status="YES")
            msg=dict(msg)
            if(msg['stat']=='Ok' or msg['stat']=='ok'):
                if("NOrdNo" in msg.keys()):
                    orderNumber=msg['NOrdNo']
                    Order_status=dict(order_history(User,orderNumber)[0])
                    if(Order_status['Status']=="rejected"):
                        Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                        Status = Status.replace("-","")
                        cancel_obj=CanceledOrders(Chart_Symbol=open_obj.Chart_Symbol,Quantity=open_obj.Quantity,
                        Order_Number=orderNumber,status=Status,
                        Execution_Time=str(Order_status['ExchTimeStamp']))
                        cancel_obj.User=request.user
                        cancel_obj.save()      
                    return Response({
                        "Status":200,
                        "Message":str(msg)
                    }, status=status.HTTP_201_CREATED)                           
            
                else:
                        Resp = {
                            'Status': '200',
                            'Message': str(msg)
                        }
                        return Response(Resp,status=status.HTTP_201_CREATED)
            else:
                return Response({
                            "Status":200,
                            "Message":str(msg)
                        }, status=status.HTTP_201_CREATED) 
                            
        except Exception as e:
            return Response({
                "Status":400,
                "Messsage":str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


            