from django.db import models

from mailing.models import Mailing

NULLABLE = {'blank': True, 'null': True}


class Logging(models.Model):
    ATTEMPT_OK = 'ok'
    ATTEMPT_ERROR = 'error'

    ATTEMPT_STATUS = (
        (ATTEMPT_OK, 'Удачная попытка'),
        (ATTEMPT_ERROR, 'Неудачная попытка')
    )

    last_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name='последня попытка'
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='рассылка',
        **NULLABLE
    )
    attempt_status = models.CharField(
        max_length=50,
        choices=ATTEMPT_STATUS,
        verbose_name='статус попытки',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.mailing.title}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'настройки рассылок'
