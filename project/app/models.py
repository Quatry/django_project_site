from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Project(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField('Название проекта',
                            max_length=100)
    info = models.TextField('О проекте',
                            max_length=5000)
    status = models.BooleanField(default=False)


class Participant(models.Model):
    participant = models.ForeignKey(
                                    User,
                                    on_delete=models.CASCADE,
                                    )
    invite_status = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

class ProjectUpdate(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    update = models.TextField(max_length=1000)

class ProjectEvent(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    info = models.TextField(max_length=1000)
    date = models.DateField()
    duration = models.DurationField()