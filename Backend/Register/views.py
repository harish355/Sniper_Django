from django.http import JsonResponse
from .models import Account
from .serializers import AccountSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Register(APIView):
    # def get(self, request):
    #     snippets = Account.objects.all()
    #     serializer = AccountSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
