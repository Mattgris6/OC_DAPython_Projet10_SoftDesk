from rest_framework import serializers

from itsystem.models import Project, Issue, Comment, Contributor

from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user_id']


class ProjectDetailSerializer(serializers.ModelSerializer):
    
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.filter()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag']


class IssueDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'desc',
            'tag',
            'priority',
            'status',
            'author_user_id',
            'assignee_user_id',
            'created_time',
            'comments',
        ]

    def get_comments(self, instance):
        queryset = instance.comments.filter()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'created_time']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'author_user_id']
