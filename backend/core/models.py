from django.db import models


class DummyModel(models.Model):
    """Dummy Model to test GraphQL"""
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name
