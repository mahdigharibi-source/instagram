from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """"
    قبل از رسیدن به شی ایجاد میشود به همه اجازه خواندن میدهد اما برای نوشتن شرط is_authenticated را چک میکند
    """
    def has_permissions(self, request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        وقتی میخواهید یک شی خاص را تغییر دهید اجرا میشود
        بررسی میکند که ایا obj.user با request.user.is_authenticated برابر هست یا نه
         چون این کارباعث میشود ادمین هم در سطح api نتواند پست دیگران را ویرایش کند
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user.profile