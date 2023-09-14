from django.core.management import BaseCommand

from mailing.cron import run_mailing


class Command(BaseCommand):
    help = 'Отправка запланированной рассылки'

    def add_arguments(self, parser):
        parser.add_argument('mailing_pk', type=str, help='PK рассылки')

    def handle(self, *args, **kwargs):
        mailing_pk = kwargs['mailing_pk']
        run_mailing(mailing_pk)
