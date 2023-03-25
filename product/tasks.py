from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string

from account.models import User


def message_build(sku:str, username, data:dict) -> str:
    """
    builds message to be send
    """
    msg = f"Hello! recently product: {sku} were update!\nchanges made by user: '{username}' were:\n"
    for key, value in data.items():
        msg += f"\n{key}={value}"
    return msg

@shared_task
def update_product_email(user:User, sku:str, data:dict) -> bool:
    """
    sends an e-mail to every admin user related to a product attribute update
    :param data: (dict) e-mails related info
    :return: True/False
    """
    recipients = [user.email for user in User.objects.filter(is_staff=True).only("email")]
    msg = message_build(sku=sku, username=user.username, data=data)
    send_mail("Recent Product Update",
              msg,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=recipients,
              fail_silently=False)
