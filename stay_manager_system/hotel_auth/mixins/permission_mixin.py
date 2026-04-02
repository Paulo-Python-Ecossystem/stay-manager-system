import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

logger = logging.getLogger(__name__)


class PermissionMixin(LoginRequiredMixin):
    """
    Template View Mixin to easily set custom set of permissions.
    """

    permissions = []

    def has_permissions_old(self):
        return all(self.request.user.has_perm(perm) for perm in self.get_required_permissions())

    def get_required_permissions_as_list(self):
        """
        Return all permissions required in the view as a list.

        :raises ImproperlyConfigured: if no permissions were settet in 'permissions', raises "ImproperlyConfigured".
        :return: return a list containing all configured permissions.
        :rtype: [string]
        """
        perms = self.permissions
        # logger.debug(perms)
        if callable(perms):
            perms = perms()
        # logger.debug(perms)

        if isinstance(perms, str):
            return [perms]
        if hasattr(perms, "__iter__"):
            return perms

        raise ImproperlyConfigured("Provide a 'permissions' attribute.")

    def has_permissions(self):
        """
        Verifica se o usuário autenticado tem permissão para acessar a view.

        Suporta:
        - String: única permissão
        - Lista ou tupla de strings: OR entre permissões
        - Tupla de listas/tuplas de strings: OR entre grupos de permissões (cada grupo com AND interno)
        """
        perms = self.permissions
        # logger.debug(f"PermissionMixin: {perms}")

        # Caso não tenha sido definida nenhuma permissão → acesso liberado
        if not perms:
            return True

        if isinstance(perms, str):
            return self.request.user.has_perm(perms)

        elif isinstance(perms, (list, tuple)):
            # logger.debug("perms iterable")
            if all(isinstance(p, str) for p in perms):
                # logger.debug("perms IF")
                # logger.debug(f"perms user: {self.request.user.pk} {self.request.user}")
                # logger.debug(f"perms user groups: {self.request.user.groups.first().permissions.all()}")
                # logger.debug(f"perms {list(self.request.user.has_perm(p) for p in perms)}")
                return any(self.request.user.has_perm(p) for p in perms)

            elif all(isinstance(p, (list, tuple)) for p in perms):
                # logger.debug("perms ELIF")
                return any(self.request.user.has_perms(group) for group in perms)

        raise ImproperlyConfigured(
            "O atributo 'permissions' deve ser uma string, uma lista/tupla de strings (OR), "
            "ou uma tupla de listas/tuplas de strings (grupos com AND interno)."
        )

    def dispatch(self, request, *args, **kwargs):
        """
        Check if User has parmissions to access this View page.

        :raises Http404: if user don't have required permissions raises "Http404".
        """
        if request.user.is_authenticated:
            if not self.has_permissions():
                # logger.debug("aqui negado")
                raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
