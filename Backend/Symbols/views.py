import re
from django.http import JsonResponse
from .models import Symbols
from .serializers import SymbolsSerializer,Symbols_Get_Serializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .Zebul_api_funcs import *
from User_Settings.models import Api_table
from OpenOrder.models import OpenOrders
from CancelOrder.models import CanceledOrders


Market_Choice = {
    "1": "NSE",
    "2": "BSE",
    "3":"MCX",
    "4":"NFO"
}

class Symbols_watch_list(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Symbols_list = Symbols.objects.filter(User=request.user)
        serialized_obj = Symbols_Get_Serializer(Symbols_list, many=True)
        return Response(serialized_obj.data)

    def post(self, request):
        serializer_obj = SymbolsSerializer(data=request.data)
        if serializer_obj.is_valid():
            list_obj=Symbols.objects.filter(User=request.user)
            for obj in list_obj:
                if(obj.Chart_Symbol==request.data['Chart_Symbol']):
                   return Response({
                       'Status': '400',
                        'Message': 'Symbol Already exist in your Watch list'
                   }, status=status.HTTP_400_BAD_REQUEST) 
                if(obj.Terminal_Symbol==request.data['Terminal_Symbol']):
                    return Response({
                       'Status': '400',
                        'Message': 'Same Terminal Symbol already present in watchlist'
                   }, status=status.HTTP_400_BAD_REQUEST) 
            try:
                Api_object=Api_table.objects.get(User=request.user)
                User=get_user(Api_object.userid,Api_object.api_key)
                exchange=Market_Choice[request.data['Market']]
                if(exchange=="NSE" or exchange=="BSE"):
                    token=User.get_scrips(symbol=request.data['Chart_Symbol'], exchange=[exchange])
                    if(token!=[]):
                        token=token[0]['token']
                        print(token)
                    else:
                        return Response({
                            "Status":400,
                            "Message":"Cannot Find this Symbol"
                            }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token=User.get_scrips(symbol=request.data['Chart_Symbol'], exchange=[exchange])
                    if(token!=[]):
                        token=token[0]['token']
                        print(token)
                    else:
                        return Response({
                            "Status":400,
                            "Message":"Cannot Find this Symbol"
                            }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({
                       'Status': '400',
                        'Message': str(e)
                   }, status=status.HTTP_400_BAD_REQUEST)

            saved_obj=serializer_obj.save()
            saved_obj.User=request.user
            saved_obj.Token_id=str(token)
            print(token)
            saved_obj.save()
            return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class Update_Symbols(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_obj = SymbolsSerializer(data=request.data)
        c_symbol = request.data['Chart_Symbol']
        Symbols_obj = Symbols.objects.filter(Chart_Symbol=c_symbol)
        for objs in Symbols_obj:
            if(objs.User == request.user):
                if(serializer_obj.is_valid()):
                    token=objs.Token_id
                    objs.delete()
                    saved_obj=serializer_obj.save()
                    saved_obj.User=request.user
                    saved_obj.Token_id=token
                    saved_obj.save()
                    return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'Status': '400',
                'Message': 'No Pre-existing Symbols Data'
        }, status=status.HTTP_400_BAD_REQUEST)


class Delete_Symbols(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        c_symbol = request.data['Chart_Symbol']
        Symbols_obj = Symbols.objects.filter(Chart_Symbol=c_symbol)
        for objs in Symbols_obj:
            if(objs.User == request.user):
                objs.delete()
                Resp = {
                    'Status': '200',
                    'Message': 'Success'
                }
                return Response(Resp, status=status.HTTP_201_CREATED)
        Resp = {
                'Status': '400',
                'Message': "User Doesn't have this Symbol in his watchlist "
                }
        return Response(Resp, status=status.HTTP_400_BAD_REQUEST)


class Buy_Symbols(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            chart_sym=request.data['Chart_Symbol']
            transtype=request.data["transtype"]
            Symbols_obj = Symbols.objects.filter(User=request.user)
            print(Symbols_obj)
            for obj in Symbols_obj:
                if(obj.Chart_Symbol==chart_sym):
                    Api_object=Api_table.objects.get(User=request.user)
                    User=get_user(Api_object.userid,Api_object.api_key)
                    exchange=Market_Choice[obj.Market]
                    token=obj.Token_id
                    if(exchange=="NSE" or exchange=="BSE"):
                        trading_symbol=chart_sym+"-EQ"
                    message=place_order(user=User,ret="DAY",trading_symbol=trading_symbol, exch=str(exchange), discqty=int(float(obj.Quantity)*0.1),
                    transtype=transtype, prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=obj.Limit, trigPrice=0, pCode="MIS", 
                    complexty="REGULAR")
                    print("Message: ",message)
                    
                    print(User,"DAY",token, str(exchange), int(float(obj.Quantity)*0.1),
                    transtype, "L", str(obj.Quantity), token, obj.Limit, 0, "MIS", 
                    "REGULAR")
                    
                    if("NOrdNo:" in message):

                        orderNumber=int(message.split("NOrdNo:")[1])
                        Order_status=dict(order_history(User,orderNumber)[0])

                        if(Order_status['Status']=="rejected"):
                            Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                            Status = Status.replace("-","")
                            # if("RMS" in Status):
                            #     token=User.get_scrips(symbol=chart_sym, exchange=[exchange])[0]["symbol"]
                            #     message=place_order(user=User,ret="DAY",trading_symbol=chart_sym, exch=str(exchange), discqty=int(float(obj.Quantity)*0.1),
                            #     transtype=transtype, prctyp="L", qty=str(obj.Quantity), symbol_id=token, price=obj.Limit, trigPrice=0, pCode="MIS", 
                            #     complexty="REGULAR")
                            #     if("NOrdNo:" in message):
                            #         orderNumber=int(message.split("NOrdNo:")[1])
                            #         Order_status=dict(order_history(User,orderNumber)[0])
                            #         if(Order_status['Status']=="rejected"):
                            #             Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                            #             Status = Status.replace("-","")
                            #             cancel_obj=CanceledOrders(Chart_Symbol=chart_sym,Quantity=obj.Quantity,
                            #             Order_Number=orderNumber,status=Status,
                            #             Execution_Time=str(Order_status['ExchTimeStamp']))
                            #             cancel_obj.User=request.user
                            #             cancel_obj.save()
                            #             return Response({
                            #                 'Status': '200',
                            #                 'Message': Status
                            #             }, status=status.HTTP_201_CREATED)
                                
                            #     else:
                            #             Status=str(Order_status['Status'])
                            #             Status = Status.replace("-","")
                            #             open_obj=OpenOrders(Buy_price=int(obj.Limit),Terminal_Symbol=obj.Terminal_Symbol,Quatity=int(obj.Quantity),Order_Number=orderNumber,
                            #             Status=str(Order_status['Status'],Exchange=exchange)
                            #             )
                            #             open_obj.User=request.user
                            #             open_obj.save()
                            #             Symbols_obj.delete()
                            #             return Response({
                            #                                     'Status': '200',
                            #                                     'Message': Status
                            #             }, status=status.HTTP_201_CREATED)

                            # else:
                            cancel_obj=CanceledOrders(Chart_Symbol=chart_sym,Quantity=obj.Quantity,
                            Order_Number=orderNumber,status=Status,
                            Execution_Time=str(Order_status['ExchTimeStamp']))
                            cancel_obj.User=request.user
                            cancel_obj.save()
                            return Response({
                                'Status': '200',
                                'Message': Status
                            }, status=status.HTTP_201_CREATED)
                        else:
                            Status=str(Order_status['Status'])
                            Status = Status.replace("-","")
                            open_obj=OpenOrders(Chart_Symbol=str(chart_sym),Buy_price=int(obj.Limit),Terminal_Symbol=obj.Terminal_Symbol,Quatity=int(obj.Quantity),Order_Number=orderNumber,
                            Status=str(Order_status['Status']),Exchange=exchange
                                )
                            open_obj.User=request.user
                            open_obj.save()
                            Symbols_obj.delete()
                            return Response({
                                'Status': '200',
                                'Message': Status
                            }, status=status.HTTP_201_CREATED)

                    
                    Resp = {
                        'Status': '300',
                        'Message': message
                    }
                    return Response(Resp, status=status.HTTP_201_CREATED)
            Resp = {
                'Status': '400',
                'Message': 'Symbol Data not Present'
            }
            return Response(Resp, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "Status":500,
                "Message":str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class List_of_Symbols(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        Symbol_obj=Symbols.objects.filter(User=request.user)
        Sym_list=[]
        for obj in Symbol_obj:
            temp=list([obj.Chart_Symbol,Market_Choice[obj.Market],obj.Token_id])
            if(temp not in Sym_list):
                Sym_list.append(temp)
        return Response({"List":Sym_list}, status=status.HTTP_201_CREATED)


class Buy_Sell(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            chart_sym=request.data['Chart_Symbol']
            exchange=request.data['exchange']
            Quantity=request.data['Quantity']
            order_type=request.data['order_type']
            order=request.data['order']
            trigger=request.data['trigger']
            price=request.data['price']
            transtype=request.data['transtype']
            prctyp=request.data['prctyp']
        except Exception as e:
            print(e)
            return Response({
                "Status":400,
                "Message":"Invalid Data Type"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            discqty=int(float(Quantity)*0.1)
            ret="DAY"

            if(order!="REGULAR"):
                try:
                    Target=request.data['Target']
                    Stoploss=request.data['Stoploss']
                    Trailing_Stoploss=request.data['Trailing_Stoploss']
                except:
                    return Response({
                        "Status":400,
                        "Message":"For Bracket Order, needed Target, Stoploss and Trailing_Stoploss"
                    }, status=status.HTTP_400_BAD_REQUEST)

                Api_object=Api_table.objects.get(User=request.user)
                User=get_user(Api_object.userid,Api_object.api_key)
                if(exchange=="NSE" or exchange=="BSE"):
                    token=User.get_scrips(symbol=chart_sym, exchange=[exchange])[0]["token"]
                    if(token!=[]):
                        token=token[0]['symbol']
                        print(token)
                    else:
                         return Response({
                        "Status":400,
                        "Message":"Cannot Find this Symbol"
                         }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token=User.get_scrips(symbol=chart_sym, exchange=[exchange])
                    if(token!=[]):
                        token=token[0]['symbol']
                        print(token)
                    else:
                        return Response({
                        "Status":400,
                        "Message":"Cannot Find this Symbol"
                         }, status=status.HTTP_400_BAD_REQUEST)


                if(price=="0" and trigger=="0"):
                    prctyp="MKT"
                elif(price!="0" and trigger=="0" ):
                    prctyp="L"
                elif(trigger!="0" and price=="0"):
                    prctyp="SL-M"
                else:
                    prctyp="SL"

                message=bracket_order(User,complexty=order,discqty=discqty,exch=exchange,pCode=order_type
                ,price=price,qty=Quantity,prctyp=prctyp,stopLoss=trigger,ret=ret,symbol_id=token
                ,trading_symbol=token,trailing_stop_loss=Trailing_Stoploss,target=Target,transtype=transtype,trigPrice=trigger)

                
                if(type(message)==type([])):
                    print("Bracket Order Placed")
                    if(dict(message[0])['stat']=="ok" or dict(message[0])['stat']=="Ok"):
                        orderNumber=int(dict(message[0])['NOrdNo'])
                        Order_status=dict(order_history(User,orderNumber)[0])
                        if(Order_status['Status']=="rejected"):
                            Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                            Status = Status.replace("-","")
                            cancel_obj=CanceledOrders(Chart_Symbol=chart_sym,Quantity=Quantity,
                            Order_Number=orderNumber,status=Status,
                            Execution_Time=str(Order_status['ExchTimeStamp']))
                            cancel_obj.User=request.user
                            cancel_obj.save()
                        else:
                            Status=str(Order_status['Status'])
                            Status = Status.replace("-","")
                            open_obj=OpenOrders(Buy_price=int(price),Quatity=int(Quantity),Terminal_Symbol="NULL",Order_Number=orderNumber,
                            Status=str(Order_status['Status'],Exchange=exchange)
                                )
                            open_obj.User=request.user
                            open_obj.save()
                            
                else:
                    print(message)

                Resp = {
                            'Status': '200',
                            'Message': message
                        }
                return Response(Resp, status=status.HTTP_201_CREATED)
            else:
                Api_object=Api_table.objects.get(User=request.user)
                User=get_user(Api_object.userid,Api_object.api_key)
                if(exchange=="NSE" or exchange=="BSE"):
                    token=User.get_scrips(symbol=chart_sym, exchange=[exchange])[0]["token"]
                    if(token!=[]):
                        token=token[0]['symbol']
                        print(token)
                    else:
                         return Response({
                        "Status":400,
                        "Message":"Cannot Find this Symbol"
                         }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token=User.get_scrips(symbol=chart_sym, exchange=[exchange])
                    if(token!=[]):
                        token=token[0]['instrument_name']
                        print(token)
                    else:
                        return Response({
                        "Status":400,
                        "Message":"Cannot Find this Symbol"
                         }, status=status.HTTP_400_BAD_REQUEST)

                if(price=="0" and trigger=="0"):
                    prctyp="MKT"
                elif(price!="0" and trigger=="0" ):
                    prctyp="L"
                elif(trigger!="0" and price=="0"):
                    prctyp="SL-M"
                else:
                    prctyp="SL"

                message=place_order(user=User,ret=ret,trading_symbol=token, exch=exchange, discqty="0",
                transtype=transtype, prctyp=prctyp, qty=str(Quantity), symbol_id=token, price=price, trigPrice=trigger, pCode=order_type, 
                complexty=order)

                print("Order placed")

                
                if("NOrdNo:" in     message):
                    orderNumber=int(message.split("NOrdNo:")[1])
                    Order_status=dict(order_history(User,orderNumber)[0])
                    Status=str(Order_status['Status'])
                    if(Order_status['Status']=="rejected"):
                            Status=str(Order_status['Status']+" "+Order_status['rejectionreason'])
                            Status = Status.replace("-","")
                            cancel_obj=CanceledOrders(Chart_Symbol=chart_sym,Quantity=Quantity,
                            Order_Number=orderNumber,status=Status,
                            Execution_Time=str(Order_status['ExchTimeStamp']))
                            cancel_obj.User=request.user
                            cancel_obj.save()
                            
                    else:
                            Status=str(Order_status['Status'])
                            Status = Status.replace("-","")
                            open_obj=OpenOrders(Chart_Symbol=chart_sym,Buy_price=int(price),Quatity=int(Quantity),Terminal_Symbol="NULL",Order_Number=orderNumber,
                            Status=str(Order_status['Status'],Exchange=exchange)
                                )
                            open_obj.User=request.user
                            open_obj.save()
                    print("Saved order")
                else:
                    print(message)

                Resp = {
                            'Status': '200',
                            'Message': message
                        }
                return Response(Resp, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "Status":200,
                "Message":str(e)
            }, status=status.HTTP_400_BAD_REQUEST)