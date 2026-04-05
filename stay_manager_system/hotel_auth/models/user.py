from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        # permissions = [
        #     ("view_user", "View User"),
        #     ("add_user", "Add User"),
        #     ("change_user", "Change User"),
        #     ("delete_user", "Delete User"),
        # ]

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
    )
    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email Verified",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    def __str__(self):
        return self.username


class Account(models.Model):
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        # permissions = [
        #     ("view_account", "View Account"),
        #     ("add_account", "Add Account"),
        #     ("change_account", "Change Account"),
        #     ("delete_account", "Delete Account"),
        # ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="account",
        verbose_name="User",
    )
    role = models.ForeignKey(
        "hotel_auth.Role",
        on_delete=models.CASCADE,
        related_name="account",
        verbose_name="Role",
    )

    def __str__(self):
        return f"{self.user.username} - {self.role.label}"
