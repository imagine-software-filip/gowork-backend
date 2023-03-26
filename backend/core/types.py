from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from core.models import Job, CategoryService

User = get_user_model()

class UserType(DjangoObjectType):
    """UserType for GraphQL"""
    class Meta:
        model = User
        exclude = ('password',)


class JobType(DjangoObjectType):
    """JobType"""
    class Meta:
        model = Job

class CategoricalServiceType(DjangoObjectType):
    """CategoricalServiceType"""

    class Meta:
        model = CategoryService
