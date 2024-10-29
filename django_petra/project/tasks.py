from celery import shared_task
from drf_friend.mailer.send_mail import SendMail

@shared_task()
def drf_mail(email_data):
    mail = SendMail()
    mail.from_email(email_data['from'])
    mail.to(email_data['to'])
    mail.subject(email_data["subject"])
    mail.template(template_name=email_data["template_name"], context=email_data["context"])
    mail.send()
