from django.db import models
from common.models import AbstractBaseModel

class DummyModel(models.Model):
    """Dummy Model to test GraphQL"""
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name

class User(AbstractBaseModel):
    pass