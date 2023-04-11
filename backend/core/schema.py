from graphene import Field, List, ObjectType, Schema, String
from .types import UserType, JobType, FreelancingServiceType, CategoryServiceType, FreelancingType, OfferType, ResolvedServiceType
from .mutations import UserCreate, VerifyUser, SendOffer, ChangeOfferStatus, FinishServiceByProvider, RateService, ForgotPasswordGenToken, ForgotPasswordSetNew
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from core.models import Job, Freelancing, FreelancingService, CategoryService, Offer, ResolvedService

User = get_user_model()


class Query(ObjectType):
    current_user = Field(UserType, token=String(required=True))
    users = List(UserType, token=String(required=True))
    user = List(UserType, token=String(required=True), user_pk=String(required=True))
    jobs = List(JobType, token=String(required=True))
    job = Field(JobType, token=String(required=True), job_id=String(required=True))
    freelancing = List(FreelancingType, token=String(required=True))
    freelancing_services = List(FreelancingServiceType, token=String(required=True), user_pk=String(required=True))
    one_freelancing = Field(FreelancingType, token=String(required=True), freelancing_id=String(required=True))
    category = List(CategoryServiceType, token=String(required=True))
    # Scheduling
    requestor_offers = List(OfferType, token=String(required=True), user_pk=String(required=True))
    providor_offers = List(OfferType, token=String(required=True), user_pk=String(required=True))
    accepted_offers = List(OfferType, token=String(required=True), user_pk=String(required=True))
    ready_to_rate_services = List(ResolvedServiceType, token=String(required=True), user_pk=String(required=True))

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
    def resolve_job(root, info, job_id, **kwargs):
        return Job.objects.get(pk=job_id)
    
    @login_required
    def resolve_user(root, info, user_pk ,**kwargs):
        user = User.objects.get(pk=user_pk)
        return user
    
    @login_required
    def resolve_freelancing(root, info, **kwargs):
        freelancing = Freelancing.objects.all()
        return freelancing
    
    @login_required
    def resolve_one_freelancing(root, info, freelancing_id, **kwargs):
        return Freelancing.objects.get(pk=freelancing_id)
    
    @login_required
    def resolve_freelancing_services(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        freelancing = Freelancing.objects.get(user=user)
        freelancingservice = FreelancingService.objects.filter(freelancing=freelancing)
        return freelancingservice

    @login_required
    def resolve_category(root, info, **kwargs):
        return CategoryService.objects.all()
    
    # Scheduling
    @login_required
    def resolve_requestor_offers(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        return Offer.objects.filter(requester=user)
    
    @login_required
    def resolve_providor_offers(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        return Offer.objects.filter(provider=user)
    
    @login_required
    def resolve_accepted_offers(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        return Offer.objects.filter(provider=user, status="Accepted")
    
    @login_required
    def resolve_ready_to_rate_services(root, info, user_pk, **kwargs):
        user = User.objects.get(pk=user_pk)
        offer = Offer.objects.get(requester=user)
        return ResolvedService.objects.filter(offer=offer, job_done=True)
    

class Mutation(ObjectType):
    user_create = UserCreate.Field()
    verify_user = VerifyUser.Field()
    forgot_password_gen_token = ForgotPasswordGenToken.Field()
    forgot_password_set_new = ForgotPasswordSetNew.Field()

    send_offer = SendOffer.Field()
    change_offer_status = ChangeOfferStatus.Field()
    finish_service_by_provider = FinishServiceByProvider.Field()
    rate_service = RateService.Field()
    
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)
