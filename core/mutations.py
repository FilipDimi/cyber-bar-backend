import graphene
from datetime import datetime
from django.contrib.auth import get_user_model
from .types import UserType


User = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        type = graphene.String(required=True)
        is_admin = graphene.Boolean(required=True)

    def mutate(self, info, username, email, first_name, last_name, password, type, is_admin):
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.type = type
        user.is_admin = is_admin
        user.is_staff = is_admin
        user.is_active = True

        user.save()
        
        return CreateUser(user=user)