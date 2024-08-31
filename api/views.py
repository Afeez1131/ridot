from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from knox.models import AuthToken
from rest_framework import viewsets, status
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import pagination

from api.permissions import IsAuthenticatedAdminOrAuthorOrReadOnly
from core.models import Blog
from api import serializers


class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blog posts to be created, viewed, or edited.

    retrieve:
    Retrieve a specific blog post by its ID.

    list:
    Retrieve a list of all blog posts.

    create:
    Create a new blog post. The authenticated user is set as the author.

    update:
    Update a specific blog post by its ID. Only the author or an admin can update the blog post.

    partial_update:
    Partially update a specific blog post by its ID. Only the author or an admin can update the blog post.

    destroy:
    Delete a specific blog post by its ID. Only the author or an admin can delete the blog post.
    """
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    permission_classes = [IsAuthenticatedAdminOrAuthorOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all blog posts.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new blog post.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific blog post by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a specific blog post.
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific blog post.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Override the default perform_create to set the request user as the author.
        """
        serializer.save(author=self.request.user)


class LoginViewSet(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class RegisterUserView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serialized_user = self.serializer_class(user)
            response = {
                'user': serialized_user.data,
                'message': 'User created',
                'token': AuthToken.objects.create(user)[1],
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


ListUsersView = ListUsersViewset.as_view({'get': 'list'})
