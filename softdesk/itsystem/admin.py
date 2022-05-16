from django.contrib import admin
from itsystem.models import Comment, Contributor, Project, Issue

class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'author_user_id', 'description')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'author_user_id', 'assignee_user_id', 'project_id')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('description', 'issue_id', 'author_user_id')


class ContributorAdmin(admin.ModelAdmin):

    list_diplay = ('author_user_id', 'project_id')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)