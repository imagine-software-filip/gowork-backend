from graphene_django.types import DjangoObjectType
from .models import DummyModel


class DummyType(DjangoObjectType):
    class Meta:
        model = DummyModel
        fields = ("id", "name", "level", "date")
