from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        
        try:
            token["role"] = user.account.role.label 
            token["is_staff_role"] = user.account.role.is_staff
        except Exception:
            token["role"] = None
            token["is_staff_role"] = False

        return token
