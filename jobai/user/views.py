from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from .models import User,OTP
from .send_emails import send_email
import random


# Create your views here.
class SignupApiView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        print(data)
        #print(data.username)
        try:
            user = User.objects.create_user(username=data["username"],first_name=data["first_name"],last_name=data["last_name"],email=data["email"],password=data["password"],is_active=0)
        except:
            return Response(
                {
                    "message":"Username already taken"
                }
            )
        #Send OTP
        otp = random.randint(1111,9999)
        OTP.objects.create(otp=otp,user=user)

        subject = "Signup OTP Verification"
        body = f"signup otp is {otp}"
        to_email = data["email"]
        from_email = "abhiseknanda.dev@gmail.com"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # For TLS
        login = "abhiseknanda.dev@gmail.com"
        password = "umay vqlf qxfm xspp"

        res = send_email(subject, body, to_email, from_email, smtp_server, smtp_port, login, password)

        if res == "Email sent successfully!":
            return Response(
                {
                    "status":"200 ok",
                    "message":f"Otp send sucessfully to {data["email"]}"
                }
            )
        else:
            return Response(
                {
                    "message":"There is some error try again later"
                }
            )

class VerifyOtpAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data

        try:
            user = User.objects.get(email=data["email"])
            otp = OTP.objects.get(user=user)

            if otp.otp == data["otp"]:
                user.is_active=1
                user.save()
                otp.delete()

                return Response({
                    "status":"200 ok",
                    "message":"OTP verified succesfully"
                })
            else:
                otp.delete()
                return Response(
                    {
                        "message":"Wrong otp"
                    }
                )

        except:

            return Response(
                {
                    "messgae":"OTP not found Signup again"
                }
            )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        data = request.data
        print(data)

        if not User.objects.filter(username=data["username"]).exists():
            return Response({
                "message":"Email doesn't exist"
            })

        user = authenticate(username=data["username"],password=data["password"])
        print("user",user)
        if user is None:
            return Response({
                "message": "Wrong password"
            })
        else:
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        return Response("hh")

