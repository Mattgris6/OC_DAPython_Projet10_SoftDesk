from django.db import models
from django.conf import settings


class Project(models.Model):

    TYPES = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
        ]
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Issue(models.Model):

    TAGS = [('BUG', 'BUG'), ('AMELIORATION', 'AMELIORATION'), ('TACHE', 'TACHE')]
    PRIORITIES = [('FAIBLE', 'FAIBLE'), ('MOYENNE', 'MOYENNE'), ('ELEVEE', 'ELEVEE')]
    STATUSES = [('A FAIRE', 'A FAIRE'), ('EN COURS', 'EN COURS'), ('TERMINE', 'TERMINE')]

    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, choices=TAGS)
    priority = models.CharField(max_length=255, choices=PRIORITIES)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=255, choices=STATUSES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='working_on')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    description = models.CharField(max_length=255)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Contributor(models.Model):

    class Meta:
        unique_together = ['author_user_id', 'project_id']

    def __str__(self) -> str:
        return f'{self.author_user_id} {self.project_id}'

    PERMISSIONS = (('OK', 'AUTORISE'), ('NOK', 'PAS AUTORISE'))
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributor_user')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributor_project')
    permission = models.CharField(max_length=255, choices=PERMISSIONS)
    role = models.CharField(max_length=255, blank=True)