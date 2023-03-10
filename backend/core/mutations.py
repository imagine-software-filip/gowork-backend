from graphene import Field, Mutation, String, Date
from django.contrib.auth import get_user_model
from .types import UserType

User = get_user_model()


class UserCreate(Mutation):
    """Mutation to register user"""
    user = Field(UserType)

    class Arguments:
        email = String(required=True)
        password = String(required=True)
        first_name = String(required = True)
        last_name = String(required = True)
        dob = Date(required = True)
        phone_number = String(required = True, max = 15)
        heading = String(required = True, max = 255)
        desc = String(required = True)
        image = String()

    def mutate(self, info, email, password, first_name, last_name, dob, phone_number, heading, desc, image):
        user = User(
            email=email,
            first_name = first_name, 
            last_name = last_name,
            dob = dob,
            phone_number = phone_number,
            heading = heading,
            desc = desc,
            image = image

        )
        user.set_password(password)
        user.save()

        return UserCreate(user=user)
