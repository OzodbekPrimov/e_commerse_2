
from rest_framework import permissions


class IsOwnerReadOnly(permissions.BasePermission):
    """
    Bu ruxsat faqat so'rov egasiga tahrirlash va o'chirish imkonini beradi
    qolganlarga faqat ko'rish ruxsatini (GET) beradi
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.owner == obj.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Faqat xodimlarga mahsulotni tahrirlash va o'chirishga ruxsat qolganlarga
    faqat o'qishga
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff



