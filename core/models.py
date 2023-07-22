from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from common.models import AbstractBaseModel
from backend import settings


class UserManager(BaseUserManager):
    """
    Custom User Model Manager
    """
    use_in_migrations = True

    def _create_user(self, username, email, password=None, **extra_fields):
        """
        Create a user with email and password
        """
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, username, email, password=None, **extra_fields):
        """
        User permissions
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(self, username, email, password, **extra_fields)

    def create_super_user(self, username, email, password=None, **extra_fields):
        """
        Admin Permissions
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(self, username, email, password=None, **extra_fields)

    class Meta:
        ordering = ("id")


# General Models
class User(AbstractUser, AbstractBaseModel):
    """
    Custom User Model
    """

    REQUIRED_FIELDS = ["email",]
    username = models.CharField(null=True, blank=True, unique=True, max_length=255)
    email = models.CharField(null=True, blank=True, unique=True, max_length=255)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Bar Models
class BarCategory(AbstractBaseModel):
    """
    Category for Bar
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BarSubCategory(AbstractBaseModel):
    """
    Sub Category for Bar
    """
    category = models.ForeignKey(BarCategory, on_delete=models.CASCADE, related_name="barsubcategorybarcategory")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} -> {self.category.name}"


class Beverage(AbstractBaseModel):
    """
    Beverage model
    """
    category = models.ForeignKey(BarCategory, on_delete=models.CASCADE, related_name="beveragebarcategory")
    subCategory = models.ForeignKey(BarSubCategory, on_delete=models.CASCADE, related_name="beveragesubcategory")
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#CAF1DE")
    count = models.IntegerField()
    criticalCount = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.count}/{self.criticalCount}"


class CocktailBeverage(AbstractBaseModel):
    """
    Ingrediant for a cocktail
    """
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, related_name="cocktailbeveragebeverage")
    count = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.beverage.name}"


class CocktailStep(AbstractBaseModel):
    """
    Step for a cocktail
    """
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.description[:10]}"
    

class Cocktail(AbstractBaseModel):
    """
    Craft cocktail by a user
    """
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cocktailuser")
    ingrediants = models.ManyToManyField(CocktailBeverage)
    steps = models.ManyToManyField(CocktailStep)
    color = models.CharField(max_length=10, default='#ff5335')
    glass = models.CharField(max_length=255, default="rocks")

    def __str__(self):
        return f"{self.name} by {self.creator.first_name} {self.creator.last_name}"


class BarArchive(AbstractBaseModel):
    """
    Archive to keep track of user's stocking
    """
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"


class BarTab(AbstractBaseModel):
    """
    Keep list of user's stocking
    """
    date = models.ForeignKey(BarArchive, on_delete=models.CASCADE, related_name="bartabbararchive")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bartabuser")

    def __str__(self):
        return f"{self.date.date} - {self.user.first_name} {self.user.last_name}"


class BarTabItem(AbstractBaseModel):
    """
    An item in the BarTab list
    """
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE, related_name="bartabitembeverage")
    bartab = models.ForeignKey(BarTab, on_delete=models.CASCADE, related_name="bartabitembartab")
    count = models.IntegerField()

    def __str__(self):
        return f"{self.beverage.name} -> {self.bartab.user.first_name} {self.bartab.user.last_name}"


class Thread(AbstractBaseModel):
    """
    Blog post
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    family = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threaduser")
    resolved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.user.first_name} {self.user.last_name}"


class Comment(AbstractBaseModel):
    """
    Comment for the thread
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentuser")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="commentthread")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} -> {self.thread.title}"


# # Kitchen Models
# class FoodCategory(AbstractBaseModel):
#     """
#     Category for the kitchen
#     """
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


# class FoodSubCategory(AbstractBaseModel):
#     """
#     SubCategory for the kitchen
#     """
#     category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="subfoodcategoryfoodcategory")
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.name} -> {self.category.name}"


# class Food(AbstractBaseModel):
#     category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="foodsubcategory")
#     subcategory = models.ForeignKey(FoodSubCategory, on_delete=models.CASCADE, related_name="foodsubcategory")
#     name = models.CharField(max_length=255)
#     count = models.IntegerField()

#     def __str__(self):
#         return self.name

# class KitchenArchive(AbstractBaseModel):
#     """
#     Archive to keep track of user's stocking
#     """
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.date}"


# class KitchenTab(AbstractBaseModel):
#     """
#     Keep list of user's stocking
#     """
#     date = models.ForeignKey(KitchenArchive, on_delete=models.CASCADE, related_name="kitchentabkitchenarchive")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kitchentabuser")

#     def __str__(self):
#         return f"{self.date.date} - {self.user.first_name} {self.user.last_name}"


# class KitchenTabItem(AbstractBaseModel):
#     """
#     An item in the BarTab list
#     """
#     food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="kitchentabitemfood")
#     kitchentab = models.ForeignKey(KitchenTab, on_delete=models.CASCADE, related_name="kitchentabitemkitchentab")
#     count = models.IntegerField()

#     def __str__(self):
#         return f"{self.kitchentab.user.username} - {self.food.name}"
