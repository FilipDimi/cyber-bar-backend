import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from core.types import BarCategoryType, BarSubCategoryType, BeverageType, UserType, CocktailType
from core.models import BarCategory, BarSubCategory, Beverage, Cocktail
from core.mutations import CreateUser, AddItemToTab

User = get_user_model()

# class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
#     user = graphene.Field(UserType)

#     @classmethod
#     def resolve(cls, root, info, **kwargs):
#         return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    user_create = CreateUser.Field()
    add_item = AddItemToTab.Field()


class Query(graphene.ObjectType):
    # User
    current_user = graphene.Field(UserType, token=graphene.String(required=True))

    # Categories
    all_barcategories = graphene.List(BarCategoryType)
    all_barsubcategories = graphene.List(BarSubCategoryType)
    barsubcategories_by_category = graphene.List(BarSubCategoryType, name=graphene.String(required=True))

    # Beverages
    all_beverages = graphene.List(BeverageType)
    low_beverages = graphene.List(BeverageType)
    beverages_by_category = graphene.List(BeverageType, name=graphene.String(required=True))
    beverages_by_subcategory = graphene.List(BeverageType, name=graphene.String(required=True))

    # Cocktails
    all_cocktails = graphene.List(CocktailType)
    search_cocktail = graphene.Field(CocktailType, id=graphene.String(required=True))

    # Users
    @login_required
    def resolve_current_user(root, info, **kwargs):
        user = info.context.user
        return user

    # Categories
    def resolve_all_barcategories(root, info):
        return BarCategory.objects.all()

    def resolve_all_barsubcategories(root, info):
        return BarSubCategory.objects.all()

    def resolve_barsubcategories_by_category(root, info, name):
        return BarSubCategory.objects.filter(category__name=name)

    def resolve_all_beverages(root, info):
        return Beverage.objects.all().order_by('count')
    
    def resolve_low_beverages(root, info):
        all_beverages = Beverage.objects.all().order_by('count')
        low_on_stock = []

        for beverage in all_beverages:
            if beverage.count <= beverage.criticalCount:
                low_on_stock.append(beverage)

        return low_on_stock

    # Beverages
    def resolve_beverages_by_category(root, info, name):
        return Beverage.objects.filter(category__name=name).order_by('count')

    def resolve_beverages_by_subcategory(root, info, name):
        return Beverage.objects.filter(subCategory__name=name).order_by('count')
    
    # Cocktails
    def resolve_all_cocktails(root, info):
        return Cocktail.objects.all()
    
    def resolve_search_cocktail(root, info, id):
        return Cocktail.objects.get(pk=id)


schema = graphene.Schema(query=Query, mutation=Mutation)