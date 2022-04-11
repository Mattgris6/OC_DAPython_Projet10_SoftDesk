from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from itsystem.models import Project, Comment, Issue
from itsystem.serializers import ProjectDetailSerializer, ProjectListSerializer,\
    IssueDetailSerializer, IssueListSerializer, CommentSerializer



class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminProjetViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    permission_classes = []


class ProjectViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.filter()


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        queryset = Issue.objects.filter(project_id=self.kwargs['project_pk'])
        return queryset


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        issues = Issue.objects.filter(project_id=self.kwargs['project_pk'])
        issue = issues.get(issue_id=self.kwargs['issue_pk'])
        queryset = Comment.objects.filter(issue_id=self.kwargs['issue_pk'])
        return queryset


class AdminCommentViewset(ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
