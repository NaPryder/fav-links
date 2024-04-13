from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth import login, logout, authenticate
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "is_staff"]
        read_only_fields = ["is_staff"]


class UserRegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=20, min_length=8, help_text="must be between 8 and 20 characters"
    )
    password = serializers.CharField(
        max_length=20, min_length=8, help_text="must be between 8 and 20 characters"
    )

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            # "username": {"help_text": "You help text here..."},
        }

    def validate_username(self, username):
        pattern = r"^(?![-._])(?!.*[_.-]{2})[\w.-]{8,20}(?<![-._])$"
        #     raise ValidationError("U")
        if re.match(pattern, username) is None:
            raise ValidationError("Invalid username.")

        user = User.objects.filter(username=username).last()
        if user:
            raise ValidationError(f"Username has already used")

        return username

    def validate_password(self, password):
        validators.validate_password(password)
        return password

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class SessionLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # token = None

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        print("----validate", attrs)
        if username and password:
            print("---request", self.context.get("request"))
            user1 = User.objects.get_by_natural_key(username=username)
            print("--user1", user1)
            valid = user1.check_password(raw_password=password)
            print("--valid", valid)

            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            print("--user", user)

            if not user:
                # msg = _("Unable to log in with provided credentials.")
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            # msg = _('Must include "username" and "password".')
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
