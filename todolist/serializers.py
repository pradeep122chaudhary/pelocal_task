# todo/serializers.py
from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(
        max_length=200,
        allow_blank=False,
        trim_whitespace=True
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default=''
    )

    due_date = serializers.DateField(
        required=False,
        allow_null=True
    )

    status = serializers.ChoiceField(
        choices=('pending', 'completed', 'archived'),
        default='pending'
    )

    priority = serializers.ChoiceField(
        choices=('low', 'medium', 'high', 'urgent'),
        default='medium'
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)




from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=4
    )
    email = serializers.EmailField(
        required=True,
        allow_blank=False
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password")

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("This email is already registered.")
        return email

    def validate_username(self, value):
        value = value.strip()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value


    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        validate_password(attrs["password"])
        return attrs

   

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=True
        )
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
