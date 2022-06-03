from rest_framework import permissions
from .models import Employe


PERMESSION_GLOBAL = {

}


class PermissionLevelGolbal(permissions.BasePermission):

    def allowed_employes(self) -> list[str]:
        return [Employe.DG]

    def has_permission(self, request, view):

        employe = Employe.objects.filter(user=request.user)
        return employe.status in self.allowed_employes()


class PermissionLevel_2A(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class PermissionLevel_2B(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class PermissionLevel_2C(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
