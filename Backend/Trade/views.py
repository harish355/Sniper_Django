from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from User_Settings.models import Api_table
from Symbols.models import Symbols
from User_Settings.models import Api_table
from .Zebul_api_funcs import *
from OpenOrder.models import OpenOrders
from CancelOrder.models import CanceledOrders
from CloseOrder.models import CloseOrders
from zebullconnect.zebullapi import Zebullapi
from Register.models import Account

Market_Choice = {
    "1": "NSE",
    "2": "BSE",
    "3":"MCX"
}

class Desktop_Trade(APIView):

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if(user is not None):
                token_name = request.data['token']
                order_type = request.data['type']
                order_type=order_type.upper()
                value = request.data['value']

                if("EXIT" not in order_type):
                    Symbols_obj = Symbols.objects.filter(User=user.id)
                    for obj in Symbols_obj:
                        if(obj.Terminal_Symbol==token_name):
                            Api_object=Api_table.objects.get(User=user)
                            User=get_user(Api_object.userid,Api_object.api_key)
                            exchange=Market_Choice[obj.Market]
                            token=obj.Token_id
                            
                            if("BUY" in order_type):
                                message=place_order(user=User,ret="DAY",trading_symbol=token, exch=str(exchange), discqty=int(float(obj.Quantity)*0.1),
                                transtype="BUY", prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=value, trigPrice="0", pCode="MIS", 
                                complexty="REGULAR")

                            else:
                                message=place_order(user=User,ret="DAY",trading_symbol=token, exch=str(exchange), discqty=str(obj.Quantity),
                                transtype="SELL", prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=value, trigPrice="0", pCode="MIS", 
                                complexty="REGULAR")
                            
                            if("NOrdNo:" in message):

                                orderNumber=int(message.split("NOrdNo:")[1])
                                Order_status=dict(order_history(User,orderNumber)[0])

                                if(Order_status['Status']=="rejected"):
                                    Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                                    cancel_obj=CanceledOrders(Chart_Symbol=obj.Chart_Symbol,Quantity=obj.Quantity,
                                    Order_Number=orderNumber,status=Status,
                                    Execution_Time=str(Order_status['ExchTimeStamp']))
                                    cancel_obj.User=user
                                    cancel_obj.save()
                                    Resp = {
                                    'Status': '200',
                                    'Message': Status
                                    }
                                    return Response(Resp, status=status.HTTP_201_CREATED)
                                else:
                                    Status=str(Order_status['Status'])
                                    open_obj=OpenOrders(Buy_price=int(obj.Limit),Terminal_Symbol=obj.Terminal_Symbol,Quatity=int(obj.Quantity),Order_Number=orderNumber,
                                    Status=str(Order_status['Status'],Exchange=exchange)
                                        )
                                    open_obj.User=user
                                    open_obj.save()
                                    Symbols_obj.delete()
                                    Resp = {
                                    'Status': '200',
                                    'Message': Status
                                    }
                                    return Response(Resp, status=status.HTTP_201_CREATED)
                            else:
                                Resp = {
                                    'Status': '200',
                                    'Message': message
                                }
                                return Response(Resp, status=status.HTTP_201_CREATED)
                    return Response({
                         'Status': '200',
                        'Message': "Not found"
                    }, status=status.HTTP_201_CREATED)    
                else:
                        open_obj=OpenOrders.objects.filter(User=user).order_by('-order_placed_time')
                        for o_obj in open_obj:
                            if(o_obj.Terminal_Symbol==token_name):
                                Api_object=Api_table.objects.get(User=user)
                                User=get_user(Api_object.userid,Api_object.api_key)
                                exchange=Market_Choice[obj.Market]
                                if("SUCCESS" in str(o_obj.Status).upper()):
                                    msg=squareoff_positions(user=User,exchange=o_obj.Exchange,symbol=o_obj.Chart_Symbol,
                                    qty=o_obj.Quantity,pCode="L",
                                    tokenno=o_obj.Token_id)
                                    Curr_price=user.scrips_details(exchange=exchange, token=o_obj.Token_id)['LTP']
                                    msg=dict(msg)
                                    if(msg['stat']=='Ok' or msg['stat']=='ok'):
                                        if("NOrdNo" in msg.keys()):
                                            orderNumber=msg['NOrdNo']
                                            Order_status=dict(order_history(User,orderNumber)[0])
                                            if(Order_status['Status']=="rejected"):
                                                Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                                                Status = Status.replace("-","")
                                                cancel_obj=CanceledOrders(Chart_Symbol=o_obj.chart_sym,Quantity=o_obj.Quantity,
                                                Order_Number=orderNumber,status=Status,
                                                Execution_Time=str(Order_status['ExchTimeStamp']))
                                                cancel_obj.User=user
                                                cancel_obj.save()
                                                Resp = {
                                                'Status': '200',
                                                'Message': Status
                                                }
                                                return Response(Resp, status=status.HTTP_201_CREATED)
                                            else:
                                                Status=str(Order_status['Status'])
                                                Status = Status.replace("-","")
                                                
                                                profit=(float(Curr_price)-float(o_obj.value))*int(o_obj.Quantity)
                                                Close_obj=CloseOrders(Buy_price=int(o_obj.value),Quatity=int(o_obj.Quantity),Order_Number=orderNumber,
                                                Profit=profit,
                                                Status=str(Order_status['Status'],Exchange=exchange)
                                                    )
                                                Close_obj.User=user
                                                Close_obj.save()
                                                Resp = {
                                                'Status': '200',
                                                'Message': Status
                                                }
                                                return Response(Resp, status=status.HTTP_201_CREATED)
                                                
                                    Resp = {
                                                    'Status': '200',
                                                    'Message': "Order Unsucessful"
                                                    }
                                    return Response(Resp, status=status.HTTP_201_CREATED)

                                elif("OPEN" in str(o_obj.Status).upper()):
                                    msg=exitboorder(user=User,nestOrderNumber=o_obj.Order_Number,symbolOrderId=o_obj.Token_id,status="OPEN")
                                    Curr_price=user.scrips_details(exchange=exchange, token=o_obj.Token_id)['LTP']
                                    msg=dict(msg)
                                    if(msg['stat']=='Ok' or msg['stat']=='ok'):
                                        if("NOrdNo" in msg.keys()):
                                            orderNumber=msg['NOrdNo']
                                            Order_status=dict(order_history(User,orderNumber)[0])
                                            if(Order_status['Status']=="rejected"):
                                                Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                                                Status = Status.replace("-","")
                                                cancel_obj=CanceledOrders(Chart_Symbol=o_obj.chart_sym,Quantity=o_obj.Quantity,
                                                Order_Number=orderNumber,status=Status,
                                                Execution_Time=str(Order_status['ExchTimeStamp']))
                                                cancel_obj.User=user
                                                cancel_obj.save() 
                                                Resp = {
                                                        'Status': '200',
                                                        'Message': Status
                                                        }
                                                return Response(Resp, status=status.HTTP_201_CREATED)   
                                    return Response({
                                        'Status':'200',
                                        'Message': "Order UnSucessful"
                                    }, status=status.HTTP_201_CREATED)                               
            
                                else:
                                        Resp = {
                                            'Status': '200',
                                            'Message': "Order Failed"
                                            
                                        }
                                        return Response(Resp, status=status.HTTP_201_CREATED)  
                            else:
                                Resp = {
                                    'Status': '200',
                                    'Message': "There is no Postion to exit"
                                }
                                return Response(Resp, status=status.HTTP_201_CREATED)

            else:
                Resp = {
                       'Status': '200',
                       'Message': "User Credentials didn't match"
                }
                return Response(Resp, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                "Status":400,
                "Message":str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


        Resp = {
            'Status': '400',
            'Message': 'Error'
        }
        return Response(Resp, status=status.HTTP_201_CREATED)


class Login(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if(user is not None):
            Resp = {
                'Status': '200',
                'Message': 'Success'
            }
            return Response(Resp, status=status.HTTP_201_CREATED)

        Resp = {
            'Status': '400',
            'Message': 'Error'
        }

        return Response(Resp, status=status.HTTP_201_CREATED)
