import random, string
from graphene import Field, Mutation, String, Int
from datetime import datetime
from django.contrib.auth import get_user_model
from core.models import VerifyTokenGen, Offer, ResolvedService
from .types import UserType, OfferType, ResolvedServiceType

User = get_user_model()

# HELPER FUNCTIONS
def generate_random_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ##############
# #### AUTH ####
# ##############

class UserCreate(Mutation):
    """Mutation to register user"""
    user = Field(UserType)

    class Arguments:
        email = String(required=True)
        password = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        phone_number = String(required=True)

    def mutate(self, info, email, password, first_name, last_name, phone_number, heading, desc):
        user = User(
            email=email,
            first_name = first_name, 
            last_name = last_name,
            phone_number = phone_number,
            heading = heading,
            desc = desc,
        )
        user.set_password(password)
        user.save()

        token = VerifyTokenGen()
        token.user = user
        token.token = generate_random_token()
        token.save()
        # TODO Token has to be send to the user's email

        return UserCreate(user=user)

    

class VerifyUser(Mutation):
    """Verify the users email address"""
    user = Field(UserType)

    class Arguments:
        user_id = String(required=True)
        verify_code = String(required=True)

    def mutate(self, info, user_id, verify_code):
        """Checks if the verify code is the same as the one in the db"""
        temp_user = User.objects.get(pk=user_id)
        temp_token = VerifyTokenGen.objects.get(user=temp_user)
        
        if (temp_token.token == verify_code and temp_token.is_active):
            temp_user.is_verified = True
            temp_token.is_active = False
            temp_user.save()
            temp_token.save()

            return VerifyUser(user=temp_user)
        raise Exception('Invalid Token')
    

class ForgotPasswordGenToken(Mutation):
    """Feature to reset users password"""
    user = Field(UserType)

    class Arguments:
        email = String(required=True)

    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
            token = VerifyTokenGen.objects.get(user=user)
            token.is_active = True
            token.token = generate_random_token()
            token.save()
            return ForgotPasswordGenToken(user=user)
            # Send the token to their email
        except User.DoesNotExist:
            return Exception('User with that email does not exist')
        

class ForgotPasswordSetNew(Mutation):
    """If their token match, they can set new password"""
    user = Field(UserType)

    class Arguments:
        email = String(required=True)
        token = String(required=True)
        password = String(required=True)

    def mutate(self, info, email, token, password):
        try:
            user = User.objects.get(email=email)
            verifyToken = VerifyTokenGen(user=user)

            if verifyToken.token == token:
                user.set_password(password)
                user.save()
                return ForgotPasswordSetNew(user=user)
            else:
                return Exception("Invalid token")

        except User.DoesNotExist:
            return Exception('User with that email does not match')
        

class CompleteProfile(Mutation):
    """After registration user can fill information about themselfs"""
    user = Field(UserType)

    class Arguments:
        user_pk = String(required=True)
        heading = String(required=True)
        desc = String(required=True)
        occupation = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        phone_number = String(required=True)

    def mutate(self, info, user_pk, heading, desc, occupation, first_name, last_name, phone_number):
        user = User.objects.get(pk=user_pk)
        user.heading = heading
        user.desc = desc
        user.occupation = occupation
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        return CompleteProfile(user=user)


# ####################
# #### Scheduling ####
# ####################

class SendOffer(Mutation):
    """Send an offer from a requester to provider"""
    """Creates an offer and ResolvedService. ResolvedService is used later for reviews"""
    offer = Field(OfferType)

    class Arguments:
        requester_id = String(required=True)
        provider_id = String(required=True)
        book_date = String(required=True)
        book_time = String(required=True)
        message = String(required=True)

    def mutate(self, info, requester_id, provider_id, book_date, book_time, message):
        try:
            offer = Offer()
            offer.requester = User.objects.get(pk=requester_id)
            offer.provider = User.objects.get(pk=provider_id)
            offer.message = message
            offer.book_date = datetime.strptime(book_date, '%y/%m/%d')
            offer.book_time = datetime.strptime(book_time, '%H:%M')
            offer.status = 'Pending'
            offer.save()

            service = ResolvedService()
            service.offer = offer
            service.requester = offer.requester
            service.provider = offer.provider
            service.save()

            return SendOffer(offer=offer)
        except:
            raise Exception('Something went wrong with the offer')
        

class ChangeOfferStatus(Mutation):
    """The offer can be either accepted or declined"""
    offer = Field(OfferType)

    class Arguments:
        offer_id = String(required=True)
        status = String(required=True)

    def mutate(self, info, offer_id, status):
        offer = Offer.objects.get(pk=offer_id)
        offer.status = status
        offer.save()


class FinishServiceByProvider(Mutation):
    """The provider has to mark the job as done"""
    job = Field(ResolvedServiceType)

    class Arguments:
        service_id = String(required=True)

    def mutate(self, info, service_id):
        service = ResolvedService.objects.get(pk=service_id)
        service.job_done = True
        service.save()

        return FinishServiceByProvider(job=service)


class RateService(Mutation):
    """If the ResolvedService is checked, it means it's done"""
    """Whenever the service is done, the requester can rate it"""
    service = Field(ResolvedServiceType)

    class Arguments:
        service_id = String(required=True)
        stars = Int(required=True)
        review = String(required=False)

    def mutate(self, info, service_id, stars, review):
        if stars > 5 or stars < 1:
            raise Exception('The rating must be between 1 and 5')
        service = ResolvedService.objects.get(pk=service_id)
        service.stars = stars
        service.review = review
        service.save()

        return RateService(service=service)