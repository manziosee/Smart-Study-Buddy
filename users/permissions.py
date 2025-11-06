from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers to edit content.
    """

    def has_permission(self, request, view):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for teachers
        return request.user.is_authenticated and request.user.is_teacher

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to the owner of the object
        return obj.user == request.user

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher