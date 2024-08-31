from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAdminOrAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    Other users can only read the post.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user or request.user.is_superuser
