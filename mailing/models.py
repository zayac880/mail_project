from django.db import models

from contacts.models import Contacts, ContactsList, Lists
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name='название рассылки',
        **NULLABLE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        **NULLABLE
    )
    message_title = models.CharField(
        max_length=255,
        verbose_name='тема сообщения',
        **NULLABLE
    )
    message_content = models.TextField(
        **NULLABLE,
        verbose_name='сообщение',
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='дата изменения'
    )

    setting = models.OneToOneField(
        'MailingSettings',
        on_delete=models.SET_NULL,
        related_name='mailing_settings',
        **NULLABLE,
        verbose_name='настройки рассылки'
    )
    contact_list = models.ForeignKey(
        Lists,
        on_delete=models.CASCADE,
        verbose_name='Списки контактов',
        **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingSettings(models.Model):
    MAILING_DAILY = 'daily'
    MAILING_WEEKLY = 'weekly'
    MAILING_MONTHLY = 'monthly'

    MAILING_PERIODS = (
        (MAILING_DAILY, 'Раз в день'),
        (MAILING_WEEKLY, 'Раз в неделю'),
        (MAILING_MONTHLY, 'Раз в месяц')
    )

    MAILING_NEW = 'new'
    MAILING_RUNNING = 'running'
    MAILING_COMPLETED = 'completed'

    MAILING_STATUSES = (
        (MAILING_NEW, 'новая'),
        (MAILING_RUNNING, 'запущена'),
        (MAILING_COMPLETED, 'завершена'),
    )

    mailing = models.OneToOneField(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='рассылка',
        **NULLABLE,
    )
    mailing_periods = models.CharField(
        max_length=50,
        choices=MAILING_PERIODS,
        verbose_name='периодичность рассылки',
        **NULLABLE,
    )
    status = models.CharField(
        max_length=50,
        choices=MAILING_STATUSES,
        verbose_name='статус рассылки',
        **NULLABLE,

    )
    start_date = models.DateField(
        **NULLABLE,
        verbose_name='дата начала'
    )
    mailing_time = models.TimeField(
        verbose_name='время рассылки',
        **NULLABLE
    )
    mailing_week_day_num = models.IntegerField(
        verbose_name='день недели',
        **NULLABLE,
    )

    end_date = models.DateField(
        **NULLABLE,
        verbose_name='дата окончания'
    )
    cron_setting = models.TextField(
        **NULLABLE,
        verbose_name='настройка CRON'
    )

    def __str__(self):
        return f'{self.mailing.title}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'настройки рассылок'

