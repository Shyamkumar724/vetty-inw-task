from rest_framework import serializers
from django.contrib.auth import get_user_model


class SignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(max_length=30, required=True)
    password = serializers.CharField(max_length=30, required=True, write_only=True)
    confirm_password = serializers.CharField(
        max_length=30, required=True, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "password", "confirm_password")

    def validate_first_name(self, value):
        if value is None:
            raise serializers.ValidationError({"first_name": "Cannot be Empty"})
        elif value:
            if not value.isalpha():
                raise serializers.ValidationError(
                    {"first_name": "First Name cannot Contain Numbers or Space"}
                )
        return value

    def validate_last_name(self, value):
        if value is None:
            raise serializers.ValidationError({"last_name": "Cannot be Empty"})
        elif value:
            if not value.isalpha():
                raise serializers.ValidationError(
                    {"last_name": "Last Name cannot Contain Numbers or Space"}
                )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if get_user_model().objects.filter(email=attrs.get("email")):
            raise serializers.ValidationError({"email": "Email Already Present"})
        if password != confirm_password:
            raise serializers.ValidationError(
                {"Password": "Password and Confirm Password Not Matching"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, max_length=30, write_only=True)
    password = serializers.CharField(required=True, max_length=30, write_only=True)
