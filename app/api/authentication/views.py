from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime, timedelta
from ..helpers.renderers import RequestJSONRenderer
from .serializers import RegistrationSerializer,RetriveUserSerializer
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE
from .serializers import (RegistrationSerializer, LoginSerializer,
      UserRetriveUpdateSerializer)
from .tasks import send_mail_
from .models import User
from ..helpers.token import get_token_data
from .serializers import LoginSerializer
from ..helpers.constants import (
    SIGNUP_SUCCESS_MESSAGE, VERIFICATION_SUCCESS_MSG, PASS_RESET_MESSAGE)
import jwt

class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        data = serializer.data

        user_email = data['email']
        first_name = data['first_name']


        date = datetime.now() + timedelta(hours=settings.TOKEN_EXP_TIME)
        user = User.objects.get(email=user_email)

        payload = {
            'email': user_email,
            'exp': int(date.strftime('%s')),
            'id': user.id,
            "username": data['username']
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


        domain = settings.VERIFY_URL
        url = domain + token

        body = render_to_string('verify.html', {
            'link': url,
            'first_name': first_name
        })
        subject = 'Verify your email'
        message = 'Please verify your account.'
        # send email to the user for verification
        send_mail_.delay(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user_email],
            html_message=body,
            fail_silently=False,)
        return_message = {'message': SIGNUP_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)



class ProfileApiView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RetriveUserSerializer

    def get(self, request):
        user = request.user
        user_obj = User.objects.get(pk=user.id)
        serializer = self.serializer_class(user_obj)
        data = serializer.data
        return_message = {
            "message": "Profile retrieved succesfully",
            "data":data
        }
        return Response(return_message, status=status.HTTP_200_OK)


class RetrieveUserApiView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def get(self, request, user_id):
        user_obj = User.objects.get(pk=user_id)
        serializer = self.serializer_class(user_obj)
        return_message = {
            "message": "Profile retrieved succesfully",
            "data": serializer.data
        }
        return Response(return_message, status=status.HTTP_200_OK)


class VerifyAPIView(generics.RetrieveAPIView):
    """
    A class to verify user using the token sent to the email
    """
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    @classmethod
    def get(self, request, token):
        """
        Overide the default get method
        """
        user = get_token_data(token)
        user.is_active = True
        user.save()
        return Response(data={"message": VERIFICATION_SUCCESS_MSG},
                        status=status.HTTP_200_OK)


class LoginAPIView(generics.CreateAPIView):#anyone is allowed to do this(AllowAny)
    #but to enter in you should give matching details.
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Handle user login
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = UserRetriveUpdateSerializer

    def get(self, request, *args, **kwargs):
        """
        retrieve user details from the token provided
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        overide the default patch() method to enable
        the user update their details
        """
        data = request.data

        serializer = self.serializer_class(
            request.user, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
