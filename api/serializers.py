from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from core.models import Blog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['pk', 'username', 'password']

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError('First name is required')
        if not value.isalpha():
            raise serializers.ValidationError('First name must be alphabetic')
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError('Last name is required')
        if not value.isalpha():
            raise serializers.ValidationError('Last name must be alphabetic')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        return user


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = ['pk', 'author', 'title', 'content', 'created', 'updated']
        read_only_fields = ['pk']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
