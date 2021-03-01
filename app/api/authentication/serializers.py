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
