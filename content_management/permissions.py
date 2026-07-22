from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "admin" and request.user.status == "approved")
    
class IsApprovedInstructor(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "instructor" and request.user.status == "approved")
    
class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.user.role == "admin")