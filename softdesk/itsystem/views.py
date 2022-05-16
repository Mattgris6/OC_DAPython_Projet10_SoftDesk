from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status

from itsystem.models import Project, Comment, Issue, Contributor
from itsystem.serializers import ProjectDetailSerializer, ProjectListSerializer, ProjectCreateSerializer,\
    IssueDetailSerializer, IssueListSerializer, IssueCreateSerializer, CommentSerializer,\
        CommentCreateSerializer, ContributorSerializer, UserSerializer, RegisterSerializer
from itsystem.permissions import ProjectPermissions, ContributorPermissions, IssueCommentPermissions


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class MultipleSerializerMixin:

    detail_serializer_class = None
    create_serializer_class = None

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['create', 'update'] and self.create_serializer_class is not None:
            return self.create_serializer_class
        elif self.action in ['retrieve', 'create', 'update', 'delete'] and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    create_serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def get_queryset(self):
        return Project.objects.filter(contributor_project__author_user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save(author_user_id=request.user)
            Contributor.objects.create(author_user_id=request.user, project_id=project, role='AUTHOR')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    create_serializer_class = IssueCreateSerializer
    permission_classes = [IsAuthenticated, IssueCommentPermissions]

    def get_queryset(self):
        queryset = Issue.objects.filter(project_id=self.kwargs['project_pk'])
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = IssueCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                project_id=Project.objects.get(issues=self.kwargs['project_pk']),
                author_user_id=request.user,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentSerializer
    create_serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    
    def get_queryset(self):
        queryset = Comment.objects.filter(
            issue_id__project_id=self.kwargs['project_pk'],
            issue_id=self.kwargs['issue_pk'],
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                issue_id=Issue.objects.get(pk=self.kwargs['issue_pk']),
                author_user_id=request.user,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_queryset(self):
        queryset = Contributor.objects.filter(
            project_id=self.kwargs['project_pk'],
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                project_id=Project.objects.get(pk=self.kwargs['project_pk']),
                )
        return Response(serializer.data, status=status.HTTP_201_CREATED)