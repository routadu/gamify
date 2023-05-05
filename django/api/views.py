from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics, status
from .serializers import *
from .models import User, GameProgress
from oauth2_provider.views.generic import ProtectedResourceView
from django.views.generic import TemplateView

# Create your views here.


class GameProgressUpdateView(ProtectedResourceView):

    def post(self, request, format=None):
        try:
            username = request.POST.get('username')
            gameID = request.POST.get('gameID')
            levelInc = request.POST.get('levelIncrement')
            if (username != None and gameID != None and levelInc != None):
                gameProgressQuerySet = GameProgress.objects.filter(
                    username=username,
                    gameID=gameID
                )
                gp = GameProgress()
                if (len(gameProgressQuerySet) == 0):
                    gp.username = username
                    gp.gameID = gameID
                    gp.level = levelInc
                    gp.save()
                else:
                    gp = gameProgressQuerySet[0]
                    gp.level = levelInc
                    gp.save()
                return Response({"Status": "okay"}, status=status.HTTP_200_OK)

            else:
                return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": "Exception occured", "Details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameProgressView(ProtectedResourceView):

    def post(self, request, format=None):
        try:
            username = request.POST.get('username')
            gameID = request.POST.get('gameID')
            if (username != None and gameID != None):
                gameProgressQuerySet = GameProgress.objects.filter(
                    username=username,
                    gameID=gameID
                )
                if (len(gameProgressQuerySet) == 0):
                    return Response({"Error": "Record not found"}, status=status.HTTP_417_EXPECTATION_FAILED)
                else:
                    return Response(
                        GameProgressSerializer(gameProgressQuerySet[0]).data, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": "Exception occured", "Details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(ProtectedResourceView):

    serializer_class = UserNameSerializer

    def post(self, request, format=None):
        try:
            username = request.POST.get('username')
            if (username != None):
                userQuerySet = User.objects.filter(username=username)
                if (len(userQuerySet) > 0):
                    return Response(UserProfileDetailsSerializer(userQuerySet[0]).data, status=status.HTTP_200_OK)
                else:
                    return Response({"User": "User not found"}, status=status.HTTP_417_EXPECTATION_FAILED)
            else:
                return Response({"Response": "Invalid response"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        age = request.POST.get('age')
        if (None not in (username, password, email, name, id)):
            userQuery = User.objects.filter(username=username, email=email)
            if (len(userQuery) == 0):
                user = User.fromUserDetails(
                    username=username,
                    password=password,
                    email=email,
                    name=name,
                    age=age,
                )
                user.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                user = userQuery[0]
                return Response({"Error": f"User already exists", "User": {
                    "username": username,
                    "created_at": user.date_joined
                }}, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    # serializer_class = UserAuthDetailsSerializer

    def post(self, request, format=None):
        # serializer = self.serializer_class(data=request.data)
        # try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if (username != None and password != None):
            userQuerySet = User.objects.filter(
                username=username)
            if (len(userQuerySet) == 0):
                return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            if (len(userQuerySet) == 1):
                if (userQuerySet[0].password == password):
                    return Response(UserProfileDetailsSerializer(userQuerySet[0]).data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"Error": "Incorrect Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({"Error": "Required parameters not provided"}, status=status.HTTP_400_BAD_REQUEST)
