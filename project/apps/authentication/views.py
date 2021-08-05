from os import stat
from re import L
import jwt
import json

from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib import auth

#rest_framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserSerializer, 
    LoginSerializer,
    FrontUserSerializer,
)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data)
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(GenericAPIView):
    serializer_class = FrontUserSerializer

    def get(self, request):
        if request.user.is_authenticated:
            data = FrontUserSerializer(request.user).data
            return Response(json.dumps(data), status=status.HTTP_200_OK)
        else:
            print("HOLY fuck user is not authenticated")
            return Response(
                data = {
                    "success": False,
                    "msg": "what the fuck",
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class TwoFAPage(View):

    def get(self, request, *args, **kwargs):
        return render(request, "entry.html", context={})

    def post(self, requeset, *args, **kwargs):
        data = {"receptor": phone_number,
            "token": get_token(user),
            "template": "entery",
        }