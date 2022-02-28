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

import traceback


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
                    Symbols_obj = Symbols.objects.filter(User=user)
                    for obj in Symbols_obj:
                        if(obj.Terminal_Symbol==token_name):
                            Api_object=Api_table.objects.get(User=user)
                            User=get_user(Api_object.userid,Api_object.api_key)
                            exchange=Market_Choice[obj.Market]
                            token=obj.Token_id
                            print(token)
                            if(exchange=="NSE" or exchange=="BSE"):
                                trading_symbol=obj.Chart_Symbol+"-EQ"
                            else:
                                trading_symbol=obj.Chart_Symbol
                            if("BUY" in order_type):
                                message=place_order(user=User,ret="DAY",trading_symbol=trading_symbol, exch=str(exchange), discqty=int(float(obj.Quantity)*0.1),
                                transtype="BUY", prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=value, trigPrice="0", pCode="MIS", 
                                complexty="REGULAR")

                            else:
                                message=place_order(user=User,ret="DAY",trading_symbol=trading_symbol, exch=str(exchange), discqty=str(obj.Quantity),
                                transtype="SELL", prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=value, trigPrice="0", pCode="MIS", 
                                complexty="REGULAR")
 
                            if("NOrdNo:" in message):
                                orderNumber=int(message.split("NOrdNo:")[1])
                                Order_status=dict(order_history(User,orderNumber)[0])

                                if("rejected" in Order_status['Status']):
                                    Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                                    cancel_obj=CanceledOrders(Chart_Symbol=trading_symbol,Quantity=obj.Quantity,
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
                                    if(int(value)==0):
                                        value=scrips_details(user=User,exchange=exchange, token=obj.Token_id)['LTP']
                                    
                                    open_obj=OpenOrders(Buy_price=float(value),Chart_Symbol=trading_symbol,Token_id=token,
                                    Terminal_Symbol=obj.Terminal_Symbol,Quantity=int(obj.Quantity),Order_Number=orderNumber,
                                    Status=str(Order_status['Status']),Exchange=exchange,
                                    Execution_Time=str(Order_status['ExchTimeStamp']))
                                        
                                    open_obj.User=user
                                    open_obj.save()
                                    # Symbols_obj.delete()
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
                                exchange=o_obj.Exchange
                                trading_symbol=o_obj.Chart_Symbol
                                if("SUCCESS" in str(o_obj.Status).upper() or "COMPLETE" in str(o_obj.Status).upper()):
                                    if("BUY" in order_type):
                                        transtype="SELL"
                                    else:
                                        transtype="BUY"
                                    if(value==0):
                                        prctyp="MKT"
                                    else:
                                        prctyp="L"
                                    print("Day",o_obj.Chart_Symbol, exchange, int(o_obj.Quantity*0.1),
                                    transtype, prctyp, o_obj.Quantity, o_obj.Token_id, value, 0,
                                     "MIS", "REGULAR")
                                    msg=place_order(user=User,ret="Day",trading_symbol=trading_symbol, exch=exchange, discqty=int(o_obj.Quantity*0.1),
                                    transtype=transtype, prctyp=prctyp, qty=o_obj.Quantity, symbol_id=o_obj.Token_id, price=value, trigPrice=0,
                                     pCode="MIS", complexty="REGULAR")
                                    if(prctyp=="L"):
                                        Curr_price=value
                                    else:
                                        Curr_price=scrips_details(user=User,exchange=exchange, token=o_obj.Token_id)['LTP']
                                    if("NOrdNo:" in str(msg)):
                                        orderNumber=int(msg.split("NOrdNo:")[1])
                                        Order_status=dict(order_history(User,orderNumber)[0])
                                        if(Order_status['Status']=="rejected"):
                                            Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                                            Status = Status.replace("-","")
                                            cancel_obj=CanceledOrders(Chart_Symbol=trading_symbol,Quantity=o_obj.Quantity,
                                            Order_Number=orderNumber,status=Status,
                                            Execution_Time=str(Order_status['ExchTimeStamp']))
                                            cancel_obj.User=user
                                            cancel_obj.save()
                                            o_obj.delete()
                                            Resp = {
                                                'Status': '200',
                                                'Message': Status
                                            }
                                            return Response(Resp, status=status.HTTP_201_CREATED)
                                        else:
                                            Status=str(Order_status['Status'])
                                            Status = Status.replace("-","")
                                                
                                            profit=(float(Curr_price)-float(o_obj.Buy_price))*int(o_obj.Quantity)
                                            if(transtype=="BUY"):
                                                profit=profit*-1
                                            Close_obj=CloseOrders(Chart_Symbol=o_obj.Chart_Symbol,Buy_price=float(o_obj.Buy_price),Quantity=int(o_obj.Quantity),Order_Number=orderNumber,
                                            Profit=profit,ClosePrice=float(Curr_price),
                                            Comment=Status,Execution_Time=str(Order_status['ExchTimeStamp']),Exit_at=float(Curr_price))
                                                
                                            Close_obj.User=user
                                            Close_obj.save()
                                            o_obj.delete()
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
                                    msg=cancel_order(user=User,exchange=exchange,nestordernmbr=o_obj.Order_Number,
                                    tradingsymbol=trading_symbol)
                                    print(msg)
                                    # msg="{'stat': 'Ok', 'Result': ' NEST Order Number :220223000041190'}"
                                    Curr_price=scrips_details(user=User,exchange=exchange, token=o_obj.Token_id)['LTP']
                                    msg=str(msg)
                                    if("NEST Order Number" in msg):
                                        orderNumber=msg.split(":")
                                        orderNumber=(orderNumber[-1]).split('}')
                                        orderNumber=str(orderNumber[0]).replace("'","")
                                        Order_status=dict(order_history(User,int(orderNumber))[0])
                                        if(Order_status['Status']=="cancelled"):
                                            Status=str(Order_status['Status'])
                                            Status = Status.replace("-","")
                                            cancel_obj=CanceledOrders(Chart_Symbol=trading_symbol,Quantity=o_obj.Quantity,
                                            Order_Number=orderNumber,status=Status,
                                            Execution_Time=str(Order_status['ExchTimeStamp']))
                                            cancel_obj.User=user
                                            cancel_obj.save() 
                                            o_obj.delete()
                                            Resp = {
                                                        'Status': '200',
                                                        'Message': Status
                                                    }
                                            return Response(Resp, status=status.HTTP_201_CREATED) 

                                      
                                    return Response({
                                        'Status':'201',
                                        'Message': "Order Cancel was UnSucessful"
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
                        Resp = {
                                            'Status': '200',
                                            'Message': "Order Not Found in Open Order"
                                            
                                        }
                        return Response(Resp, status=status.HTTP_201_CREATED)  

            else:
                Resp = {
                       'Status': '200',
                       'Message': "User Credentials didn't match"
                }
                return Response(Resp, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(traceback.format_exc())
            return Response({
                "Status":401,
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
