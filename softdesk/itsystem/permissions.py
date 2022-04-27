from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project, Contributor


class ProjectPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user


class ContributorPermissions(BasePermission):

    def has_permission(self, request, view):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.method == 'POST':
            return project.author_user_id == request.user
        return True

    def has_object_permission(self, request, view, obj):
        project = Project.objects.get(id=view.kwargs['project_pk'])
        if request.method in SAFE_METHODS:
            return True
        return project.author_user_id == request.user


class IssueCommentPermissions(BasePermission):

    def has_permission(self, request, view):
        return Contributor.objects.filter(project_id=view.kwargs['project_pk'], author_user_id=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user