import sys

from django.core.mail import send_mail

from logs.models import Logging
from mailing.models import Mailing


def run_mailing(mailing_pk=None):
    print('Running')
    if mailing_pk is None:
        if len(sys.argv) != 2:
            print("Usage: python your_script.py <newsletter_pk>")
            sys.exit(1)
        mailing_pk = sys.argv[1]

    try:
        mailing = Mailing.objects.get(pk=mailing_pk, setting__status='running')
    except Mailing.DoesNotExist:
        pass
    else:
        contacts_list = mailing.contact_list.contacts.all()
        contacts = [contact.email for contact in contacts_list]

    response = send_mail(
        subject=mailing.message_title,
        message=mailing.message_content,
        from_email=None,
        recipient_list=contacts,
    )
    if response == 1:
        attempt_status = 'ok'
    else:
        attempt_status = 'error'

    Logging.objects.create(
        mailing=mailing,
        attempt_status=attempt_status
    )
    # TODO: реализовать отправку сообщений / рассылок по крону

    # TODO: реализовать проверку статуса отправки и в случае ошибки
    #       добавить задачу крона с повторением отправки пока статус не
    #       станет OK после чего удалить дополнительную задачу
