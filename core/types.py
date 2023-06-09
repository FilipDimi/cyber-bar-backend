import graphene
from graphene_django.types import DjangoObjectType
from .models import BarCategory, BarSubCategory, Beverage, User, Cocktail, CocktailBeverage, CocktailStep


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


class CocktailBeverageType(DjangoObjectType):
    class Meta:
        model = CocktailBeverage


class CocktailType(DjangoObjectType):
    ingrediants = graphene.List(CocktailBeverageType)
    steps = graphene.List(CocktailBeverageType)

    class Meta:
        model = Cocktail
        fields = "__all__"

    @staticmethod
    def resolve_ingrediants(cocktail, *args, **kwargs):
        return cocktail.ingrediants.all()
    
    @staticmethod
    def resolve_steps(cocktail, *args, **kwargs):
        return cocktail.steps.all()
