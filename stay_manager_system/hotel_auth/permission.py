from rest_framework.permissions import BasePermission


class IsHotelAdmin(BasePermission):
    """
    Allows access only if the Role in the token is 'Admin'.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request, "auth") and request.auth:
            return request.auth.get("role") == "Admin"

        return False
