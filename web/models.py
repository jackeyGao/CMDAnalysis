from __future__ import unicode_literals

from django.db import models

# Create your models here.

AllowShellTypes = (
        ('ZS', 'ZSH'),
        ('BS', 'BASH')
        )

class Box(models.Model):
    _id = models.CharField(max_length=10, primary_key=True)
    shell = models.CharField(max_length=2,
            choices=AllowShellTypes, default=None,
            null=True, blank=True)


    def __str__(self):
        return self._id


class Command(models.Model):
    box = models.ForeignKey(Box)
    command = models.CharField(max_length=100)
    run_time = models.DateTimeField(
            null=True,
            blank=True)


    def __str__(self):
        return self.command


