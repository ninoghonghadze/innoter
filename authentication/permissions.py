from rest_framework.permissions import BasePermission


class IsPageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.get("user_id")


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.get("role") == "ADMIN"


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.get("role") == "MODERATOR"


class IsAdminOrModeratorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = request.user.get("role")

        if role == "ADMIN" or role == "MODERATOR":
            return True
        owner_id = obj.user_id if hasattr(obj, "user_id") else obj.page.user_id
        return owner_id == request.user.get("user_id")


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, dict)
