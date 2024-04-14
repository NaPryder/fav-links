from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth import login, logout, authenticate
import re


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ["url", "username", "password", "is_staff"]
        # read_only_fields = ["url", "is_staff"]
        fields = ["username", "is_staff", "email"]
        read_only_fields = fields


class UserChangePasswordSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=20, min_length=8, help_text="must be between 8 and 20 characters"
    )
    old_password = serializers.CharField(
        max_length=20,
        min_length=8,
        write_only=True,
    )
    new_password = serializers.CharField(
        max_length=20,
        min_length=8,
        help_text="must be between 8 and 20 characters",
        write_only=True,
    )
    new_password_2 = serializers.CharField(
        max_length=20,
        min_length=8,
        help_text="must be same as New password",
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["username", "old_password", "new_password", "new_password_2"]
        read_only_fields = ["username"]

    def validate_old_password(self, password):
        validators.validate_password(password)
        return password

    def validate_new_password(self, password):
        validators.validate_password(password)
        return password

    def validate_new_password_2(self, password):
        validators.validate_password(password)
        return password

    def validate(self, attrs):
        print("---validate all")
        raise ValidationError("test")

        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=20, min_length=8, help_text="must be between 8 and 20 characters"
    )
    password = serializers.CharField(
        max_length=20,
        min_length=8,
        help_text="must be between 8 and 20 characters",
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["url", "username", "password"]

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
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)
        user.save()
        return user


class SessionLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs
