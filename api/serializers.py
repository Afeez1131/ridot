import bleach
from bleach.css_sanitizer import CSSSanitizer
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
    # author = serializers.PrimaryKeyRelatedField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['pk', 'author', 'title', 'content', 'created', 'updated']
        read_only_fields = ['pk', 'author', 'created', 'updated']

    def validate_content(self, value):
        # Optional: Sanitize the HTML to ensure no harmful scripts are included
        # Define allowed HTML tags
        allowed_tags = [
            'p', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'br', 'img', 'blockquote',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code', 'pre', 'span', 'div', 'b', 'i', 'u'
        ]

        # Define allowed attributes for each tag
        allowed_attrs = {
            'a': ['href', 'title', 'rel', 'target'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'p': ['style'],
            'span': ['style'],
            'div': ['style'],
            '*': ['class'],  # Allow 'class' attribute on any tag
        }
        # Create a CSSSanitizer instance to define allowed CSS properties
        css_sanitizer = CSSSanitizer(allowed_css_properties=[
            'color', 'font-weight', 'font-size', 'text-align', 'background-color', 'margin', 'padding',
            'border', 'width', 'height', 'display'
        ])
        # Define allowed protocols to avoid `javascript:` or `data:` exploits
        allowed_protocols = ['http', 'https', 'mailto']

        # Clean the HTML input using Bleach
        clean_value = bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            protocols=allowed_protocols,
            strip=True,  # Removes any disallowed HTML rather than escaping it
            css_sanitizer=css_sanitizer
        )
        print(value)
        print('\n: ', clean_value)
        return clean_value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
