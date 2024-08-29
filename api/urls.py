from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from api import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'blog', views.BlogViewSet, basename='blog')

urlpatterns = [
    path('login', views.LoginViewSet.as_view(), name='knox_login'),
    path('logout', knox_views.LogoutView.as_view(), name='know_logout'),
    path('logout/all', knox_views.LogoutAllView.as_view(), name='know_logout_all'),
    path('users', views.ListUsersView, name='list_users'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('', include(router.urls)),
]
