from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.authtoken.models import Token
from .models import *


class TokenCheck(APIView):
    def post(self, request):
        try:
            token_value = request.data['token']
            res = Token.objects.get(key=token_value).user
            return Response({'status': True})
        except:
            return Response({'status': False})


class GetEstablishmentByToken(APIView):
    def post(self, request):
        try:
            token_value = request.data['token']
            res = Token.objects.get(key=token_value).user.pk
            establishment_id = Profile.objects.get(user_id=res).company.pk
            return Response({'establishment_id': establishment_id})
        except:
            return Response({'establishment_id': 'null'})