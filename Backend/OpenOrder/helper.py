# File for helper functions

from uuid import uuid4
import random
# import reverse_geocoder as rg


def generateUUID():
    return str(uuid4())


def generateOtp(length):
    return ''.join([f'{random.randint(0,9)}' for _ in range(length)])

# Functin to return country code given latitude and longitude


# def getLocation(latitude, longitude):
#     result = rg.search((latitude, longitude), mode=1)
#     return result[0]['cc']
