from rest_framework import permissions  


class IsProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return obj.email == request.user.email
        
    