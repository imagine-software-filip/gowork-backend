from graphene import Field, List, ObjectType, Schema, String
from .types import UserType, JobType, FreelancingServiceType, CategoryServiceType, FreelancingType
from .mutations import UserCreate, VerifyUser
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from core.models import Job, Freelancing, FreelancingService, CategoryService

User = get_user_model()


class Query(ObjectType):
    current_user = Field(UserType, token=String(required=True))
    users = List(UserType, token=String(required=True))
    user = List(UserType, token=String(required=True), user_pk=String(required=True))
    jobs = List(JobType, token=String(required=True))
    freelancing = List(FreelancingType, token=String(required=True))
    freelancing_services = List(FreelancingServiceType, token=String(required=True), user_pk=String(required=True))
    category = List(CategoryServiceType, token=String(required=True))

    @login_required
    def resolve_users(root, info, **kwargs):
        users = User.objects.all().sort()
        return users

    @login_required
    def resolve_current_user(root, info, **kwargs):
        user = info.context.user
        return user
    
    @login_required
    def resolve_jobs(root, info, **kwargs):
        return Job.objects.all()
    
    @login_required
    def resolve_user(root, info, user_pk ,**kwargs):
        user = User.objects.get(pk=user_pk)
        return user
    
    @login_required
    def resolve_freelancing(root, info, **kwargs):
        freelancing = Freelancing.objects.all()
        return freelancing
    
    @login_required
    def resolve_freelancing_services(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        freelancing = Freelancing.objects.get(user=user)
        freelancingservice = FreelancingService.objects.filter(freelancing=freelancing)
        return freelancingservice

    @login_required
    def resolve_category(root, info, **kwargs):
        return CategoryService.objects.all()
    

class Mutation(ObjectType):
    user_create = UserCreate.Field()
    verify_user = VerifyUser.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)
