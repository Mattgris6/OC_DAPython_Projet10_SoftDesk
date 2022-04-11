from rest_framework import serializers

from itsystem.models import Project, Issue, Comment, Contributor


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class ProjectDetailSerializer(serializers.ModelSerializer):
    
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.filter()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class IssueDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'author_user_id', 'assignee_user_id', 'created_time', 'comments']

    def get_comments(self, instance):
        queryset = instance.comments.filter()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']
