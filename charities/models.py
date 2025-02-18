from django.db import models
from django.db.models import Q

from accounts.models import User


# Create your models here.
class Benefactor(models.Model):
    EXPERIENCE_LEVELS = (
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Expert')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(default=0, choices=EXPERIENCE_LEVELS)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        query = self.filter(charity__user=user)
        return query

    def related_tasks_to_benefactor(self, user):
        query = self.filter(assigned_benefactor__user=user)
        return query

    def all_related_tasks_to_user(self, user):
        query = self.filter(Q(charity__user=user) | Q(assigned_benefactor__user=user) | Q(state='P'))
        return query


class Task(models.Model):
    GENDER_CHOICES = (
        ('M', "Male"),
        ('F', "Female")
    )
    STATE_CHOICES = (
        ('P', 'Pending'),
        ('D', 'Done'),
        ('A', 'Assigned'),
        ('W', 'Waiting')
    )
    assigned_benefactor = models.ForeignKey(
        Benefactor, on_delete=models.SET_NULL, null=True, blank=True
    )
    charity = models.ForeignKey(
        Charity, on_delete=models.CASCADE
    )
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    state = models.CharField(default='P', max_length=1, choices=STATE_CHOICES)
    title = models.CharField(max_length=60)

    objects = TaskManager()
