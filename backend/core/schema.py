import graphene
from .models import DummyModel
from .types import DummyType


class Query(graphene.ObjectType):
    all_dummies = graphene.List(DummyType)
    dummy_by_name = graphene.\
        Field(DummyType, name=graphene.String(required=True))

    def resolve_all_dummies(root, info):
        return DummyModel.objects.all()

    def resolve_dummy_by_name(root, info, name):
        try:
            return DummyModel.objects.get(name=name)
        except DummyModel.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
