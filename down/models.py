from django.db import models


class Task(models.Model):
    drivetype = models.CharField(max_length=20)
    url = models.CharField(max_length=500)
    size = models.PositiveIntegerField(null=True)
    confirmed = models.BooleanField(default=False)
    ip = models.CharField(max_length=15)
    time = models.DateTimeField(auto_now_add=True)
