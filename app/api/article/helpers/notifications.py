
from django.template.loader import render_to_string
from django.conf import settings

from ...social.models import Social, User
from ...authentication.tasks import send_mail_


def send_email_notification(user, recipient):
    """This user is the person logged in.
    """
    body =  f"{user.username} has Posted a new article"
    subject = 'New article'
    message = f'{user.username} has posted a new article'
    send_mail_.delay(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[recipient],
        html_message=body,
        fail_silently=False,)


def send_notifications(author):
    """Fuction that sends notifications

    Arg:
        None
    Return:
        None
    Riase:
        None
    """
    followers = Social.objects.filter(followee=author.id)
    for follower in followers:
        send_email_notification(author,follower.follower.email)
