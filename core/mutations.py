import graphene
from datetime import datetime
from django.contrib.auth import get_user_model
from .types import UserType, BarTabItemType
from .models import Beverage, BarArchive, BarTab, BarTabItem

User = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        is_admin = graphene.Boolean(required=True)

    def mutate(self, info, username, email, first_name, last_name, password, is_admin):
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_admin = is_admin
        user.is_staff = is_admin
        user.is_active = True

        user.save()
        
        return CreateUser(user=user)
    

class AddItemToTab(graphene.Mutation):
    tab = graphene.Field(BarTabItemType)

    class Arguments:
        bev_id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        count = graphene.String(required=True)

    def mutate(self, info, bev_id, user_id, count):
        item = BarTabItem()
        item.beverage = Beverage.objects.get(pk=bev_id)
        item.count = count

        try:
            temp_archive = BarArchive.objects.get(date=str(datetime.today().strftime('%Y-%m-%d')))
        except BarArchive.DoesNotExist:
            temp_archive = BarArchive()
            temp_archive.date = str(datetime.today().strftime('%Y-%m-%d'))
            temp_archive.save()

        try:
            temp_tab = BarTab.objects.get(date=temp_archive, user=User.objects.get(pk=user_id))
        except BarTab.DoesNotExist:
            temp_tab = BarTab()
            temp_tab.date = temp_archive
            temp_tab.user = User.objects.get(pk=user_id)
            temp_tab.save()

        beverage = Beverage.objects.get(pk=bev_id)
        beverage.count += int(count)
        beverage.save()


        item.bartab = temp_tab
        item.save()

        return AddItemToTab(tab=item)


# class SendTabToUsers(graphene.Mutation):
#     tab = graphene.Field(BarTabItemType)

#     class Arguments:
#         user_id = graphene.String(required=True)

#     def mutate(self, info, user_id):
#         all_beverages = Beverage.objects.all()
#         low_beverages = []
#         current_user = User.objects.get(pk=user_id)
#         users = User.objects.all()
#         user_emails = []

#         for user in users:
#             user_emails.append(user.email)

#         for beverage in all_beverages:
#             if beverage.count <= beverage.criticalCount:
#                 low_beverages.append(beverage)
        
#         print(f"Cu: {current_user.first_name} {current_user.last_name}")
#         print(user_emails)
#         print(low_beverages)

#         message = Mail(
#             from_email='f_dimitrievski@outlook.com',
#             to_emails='filipdimitrievski@protonmail.com',
#             subject='Sending with Twilio SendGrid is Fun',
#             html_content='<strong>and easy to do anywhere, even with Python</strong>')
#         try:
#             sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#             response = sg.send(message)
#             print(response.status_code)
#             print(response.body)
#             print(response.headers)
#         except Exception as e:
#             print(e)

#         current_tab = BarTabItem()
#         return SendTabToUsers(tab=current_tab)
        