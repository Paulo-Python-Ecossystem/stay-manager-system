from django.contrib import admin
from hotel_auth.models.permission import Role
from hotel_auth.models.user import Account, User

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "username",
        "email",
        "phone_number",
        "email_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "email_verified",
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "phone_number",
                    "email_verified",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "phone_number",
                    "email_verified",
                )
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")


admin.site.register(Role)
admin.site.register(Account)
