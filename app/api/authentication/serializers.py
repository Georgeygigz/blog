from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from ..helpers.serialization_errors import error_dict




class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Email"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
        }
    )

    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=True,
        allow_null=False,
        write_only=True,
        error_messages={
            'required': error_dict['required'],
            'min_length': error_dict['min_length'].format("Password", "8"),
            'max_length': 'Password cannot be more than 30 characters',
            'invalid': error_dict['invalid_password'],
        }
    )
    # Ensure that the first_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed password = serializers.RegexField()
    first_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('First name')
        }
    )

    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict['already_exist'].format("Username"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Username')
        }
    )

    # Ensure that the last_name does not have a space in between.
    # Must also contain only letters
    # with underscores and hyphens allowed
    last_name = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        allow_null=False,
        required=True,
        error_messages={
            'required': error_dict['required'],
            'invalid': error_dict['invalid_name'].format('Last name')
        }
    )

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['first_name', 'last_name','username','email',
                  'password', ]

class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)#here write_only means that you can't retrieve data.
    token = serializers.CharField(max_length=255, read_only=True)

    @staticmethod
    def validate(data):
        # The `validate` method is where we make sure that the current
        # instance of LoginSerializer is "valid". In the case of signing in a
        # user, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.

        # user = authenticate(email=email, password=password)
        user =  User.objects.filter(email=email, password=password).first()

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'token': user.token
        }