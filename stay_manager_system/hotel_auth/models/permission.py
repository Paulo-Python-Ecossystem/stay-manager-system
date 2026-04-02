from django.db import models
from django.contrib.auth.models import Group

# Create your models here.


class Role(models.Model):
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        # permissions = [
        #     ("view_role", "View Role"),
        #     ("add_role", "Add Role"),
        #     ("change_role", "Change Role"),
        #     ("delete_role", "Delete Role"),
        # ]

    label = models.CharField(verbose_name="Label", unique=True, max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="Description", max_length=256, blank=True, null=True)
    permission_group = models.ForeignKey(Group, verbose_name="Permission Group", null=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    def __str__(self):
        return self.label
    