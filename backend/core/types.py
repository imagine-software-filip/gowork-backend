from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from core.models import Job, Freelancing, FreelancingService, CategoryService, Offer, ResolvedService

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


class FreelancingType(DjangoObjectType):
    """FreelancingType"""
    class Meta:
        model = Freelancing


class FreelancingServiceType(DjangoObjectType):
    """FreelansingService"""
    class Meta:
        model = FreelancingService


class CategoryServiceType(DjangoObjectType):
    """CategoricalServiceType"""
    class Meta:
        model = CategoryService


class OfferType(DjangoObjectType):
    """OfferType"""
    class Meta:
        model = Offer


class ResolvedServiceType(DjangoObjectType):
    """ResolvedServiceType"""
    class Meta:
        model = ResolvedService