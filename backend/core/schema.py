from graphene import Field, List, ObjectType, Schema, String
from .types import UserType
from .mutations import UserCreate, VerifyUser
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh

User = get_user_model()


class Query(ObjectType):
    current_user = Field(UserType, token=String(required=True))
    users = List(UserType, token=String(required=True))

    @login_required
    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    @login_required
    def resolve_current_user(root, info, **kwargs):
        user = info.context.user
        return user
    

class Mutation(ObjectType):
    user_create = UserCreate.Field()
    verify_user = VerifyUser.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)
