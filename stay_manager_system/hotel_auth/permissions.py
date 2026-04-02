from rest_framework import permissions

class IsStaffRole(permissions.BasePermission):
    """
    Custom permission to only allow access to users with 'is_staff_role' = True defined in their Role.
    Since we embedded this in the token, we could check the token directly if we wanted, 
    but DRF simplejwt automatically puts the verified user in request.user.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check through the Account's role
        try:
            return request.user.account.role.is_staff
        except Exception:
            return False

class HasRole(permissions.BasePermission):
    """
    Allows access only to users with a specific role label.
    Usage: permission_classes = [HasRole.with_role('Receptionist')]
    """
    required_role = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        try:
            return request.user.account.role.label == self.required_role
        except Exception:
            return False

    @classmethod
    def with_role(cls, role_label):
        """
        Dynamically create a permission class with a specific role requirement.
        """
        return type(
            f'HasRole_{role_label}',
            (cls,),
            {'required_role': role_label}
        )
