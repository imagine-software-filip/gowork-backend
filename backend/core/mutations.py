from graphene import Field, Mutation, String
from django.contrib.auth import get_user_model
from core.models import VerifyTokenGen
from .types import UserType

User = get_user_model()


class UserCreate(Mutation):
    """Mutation to register user"""
    user = Field(UserType)

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    def mutate(self, info, email, password):
        user = User(
            email=email,
        )
        user.set_password(password)
        user.save()

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
