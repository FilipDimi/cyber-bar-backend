from graphene_django.types import DjangoObjectType
from .models import BarCategory, BarSubCategory, Beverage, User


class BarCategoryType(DjangoObjectType):
    class Meta:
        model = BarCategory


class BarSubCategoryType(DjangoObjectType):
    class Meta:
        model = BarSubCategory


class BeverageType(DjangoObjectType):
    class Meta:
        model = Beverage


class UserType(DjangoObjectType):
    class Meta:
        model = User
