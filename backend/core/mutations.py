from graphene import Field, Mutation, String
from django.contrib.auth import get_user_model
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
