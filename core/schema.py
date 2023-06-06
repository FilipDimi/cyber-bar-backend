import graphene
import graphql_jwt
from core.types import BarCategoryType, BarSubCategoryType, BeverageType, UserType
from core.models import BarCategory, BarSubCategory, Beverage
from core.mutations import CreateUser


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    all_barcategories = graphene.List(BarCategoryType)
    all_barsubcategories = graphene.List(BarSubCategoryType)
    barsubcategories_by_category = graphene.List(BarSubCategoryType, name=graphene.String(required=True))
    all_beverages = graphene.List(BeverageType)
    beverages_by_category = graphene.List(BeverageType, name=graphene.String(required=True))
    beverages_by_subcategory = graphene.List(BeverageType, name=graphene.String(required=True))

    # Categories
    def resolve_all_barcategories(root, info):
        return BarCategory.objects.all()

    def resolve_all_barsubcategories(root, info):
        return BarSubCategory.objects.all()

    def resolve_barsubcategories_by_category(root, info, name):
        return BarSubCategory.objects.filter(category__name=name)

    def resolve_all_beverages(root, info):
        return Beverage.objects.all()

    # Beverages
    def resolve_beverages_by_category(root, info, name):
        return Beverage.objects.filter(category__name=name)

    def resolve_beverages_by_subcategory(root, info, name):
        return Beverage.objects.filter(subCategory__name=name)


schema = graphene.Schema(query=Query, mutation=Mutation)