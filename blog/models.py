from django.db import models

from service.utils import save_picture
from users.models import User


class Posts(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.CharField(max_length=200, verbose_name='slug')
    content = models.TextField(blank=True, verbose_name='контент')
    image = models.ImageField(
        upload_to=save_picture,
        blank=True,
        verbose_name='изображение'
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='опубликован'
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name='просмотры'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('creation_date',)
