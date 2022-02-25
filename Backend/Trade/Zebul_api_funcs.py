import requests
import json
import hashlib
from zebullconnect.zebullapi import Zebullapi

def get_encryption_key(user):
    return user.getEncryptionKey()

def place_order(user,ret,trading_symbol, exch, discqty, transtype, prctyp, qty, symbol_id, price, trigPrice, pCode, complexty):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        placeorderresp = user.place_order(complexty=complexty, exch=exch, pCode=pCode, price=price, qty=qty, prctyp=prctyp,
                                          ret=ret, trading_symbol=trading_symbol, transtype=transtype, trigPrice=trigPrice, symbol_id=symbol_id, discqty=discqty)
        print(placeorderresp)
        if("NOrdNo" in str(placeorderresp)):
            return "NOrdNo: "+str(placeorderresp[0]['NOrdNo'])
        else:
            return str(placeorderresp[0]['Emsg'])
    else:
        return "User not logged in"

def get_scrips(user,symbol,exchange):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.get_scrips(symbol=symbol, exchange=[exchange])
    else:
        return "User not logged in"
    
def getmarketwatch_list(user):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.getmarketwatch_list()
    else:
        return "User not logged in"
    
def marketwatch_scripsdata(user,mwname):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.marketwatch_scripsdata(mwname)
    else:
        return "User not logged in"
    
def addscrips(user,mwname,exchange,token):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.addscrips(mwname=mwname, exchange=exchange, token=token)
    else:
        return "User not logged in"
    
def deletescrips(user,mwname,exchange,token):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.deletescrips(mwname=mwname, exchange=exchange, token=token)
    else:
        return "User not logged in"
    
def scrips_details(user,exchange,token):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.scrips_details(exchange=exchange, token=token)
    else:
        return "User not logged in"
    
def positionbook(user,ret):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.positionbook(ret=ret)
    else:
        return "User not logged in"
    
def squareoff_positions(user,exchange,symbol,qty,pCode,tokenno):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.squareoff_positions(exchange=exchange, symbol=symbol,qty=qty,pCode=pCode,tokenno=tokenno)
    else:
        return "User not logged in"
    
def bracket_order(user,complexty,discqty,exch,pCode,price,qty,prctyp,stopLoss,ret,symbol_id,trading_symbol,trailing_stop_loss,target,transtype,trigPrice):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.bracket_order(complexty=complexty, discqty=discqty,exch=exch,pCode=pCode, price=price, qty=qty,prctyp=prctyp, stopLoss=stopLoss,ret=ret,symbol_id=symbol_id,trading_symbol=trading_symbol,trailing_stop_loss=trailing_stop_loss,target=target,transtype=transtype,trigPrice=trigPrice)
    else:
        return "User not logged in"
    
def order_data(user):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.order_data()
    else:
        return "User not logged in"
    
def tradebook(user):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.tradebook()
    else:
        return "User not logged in"
    
def exitboorder(user,nestOrderNumber,symbolOrderId,status):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.exitboorder(nestOrderNumber=nestOrderNumber,symbolOrderId=symbolOrderId, status=status)
    else:
        return "User not logged in"
    
def modifyorder(user,discqty,qty,exch,filledQuantity,nestOrderNumber,prctyp,price,trading_symbol,trigPrice,transtype,pCode):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.modifyorder(discqty=discqty, qty=qty, exch=exch,filledQuantity=filledQuantity,nestOrderNumber=nestOrderNumber, prctyp=prctyp,price=price,trading_symbol=trading_symbol, trigPrice=trigPrice,transtype=transtype, pCode=pCode)
    else:
        return "User not logged in"
    
def marketorder(user,complexty,discqty,exch,pCode,prctyp,price,qty,ret,symbol_id,trading_symbol,transtype,trigPrice):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.marketorder(complexty=complexty, discqty=discqty,exch=exch,pCode=pCode,prctyp=prctyp, price=price, qty=qty,ret=ret,symbol_id=symbol_id, trading_symbol=trading_symbol,transtype=transtype,trigPrice=trigPrice)
    else:
        return "User not logged in"
    
def cancel_order(user,exchange,nestordernmbr,tradingsymbol):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.cancel_order(exchange=exchange, nestordernmbr=nestordernmbr,tradingsymbol=tradingsymbol)
    else:
        return "User not logged in"
    
def order_history(user,nextorder):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.order_history(nextorder=nextorder)
    else:
        return "User not logged in"
    
def holdingsdata(user):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.holdingsdata()
    else:
        return "User not logged in"
    
def fundsdata(user):
    response = user.getEncryptionKey()
    if type(response)==dict and response['stat']=='Ok':
        return user.fundsdata()
    else:
        return "User not logged in"


def get_user(user_id,api_key):

    user=Zebullapi(user_id=str(user_id),api_key=str(api_key))
    return user

# place_order(user,user.RETENTION_DAY,'100',user.EXCHANGE_NSE,'0',user.BUY_ORDER,user.LIMIT_ORDER,'1','13611','1','1',"MIS",user.REGULAR_ORDER)