from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Lists(models.Model):
    """
    Represents lists of contacts.

    Attributes:
        name (str): The name of the list.
        date_added (datetime): The date and time when the list was created.

    Meta:
        verbose_name (str): The singular name for this model in the
        admin interface.
        verbose_name_plural (str): The plural name for this model in
        the admin interface.
        ordering (tuple): The default sorting order for instances of
        this model.
    """
    name = models.CharField(max_length=100, verbose_name='название списка')
    contacts = models.ManyToManyField(
        'Contacts',
        through='ContactsList'
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='список',
        **NULLABLE
    )

    def delete(self, *args, **kwargs):
        contacts_in_list = ContactsList.objects.filter(list=self)

        for contacts_list in contacts_in_list:
            other_lists = ContactsList.objects.filter(
                contact=contacts_list.contact
            ).exclude(list=self)

            if not other_lists.exists():
                contacts_list.contact.delete()

        super(Lists, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'список'
        verbose_name_plural = 'списки'
        ordering = ('date_added',)


class Contacts(models.Model):
    """
    Represents users contacts.

    Attributes:
        telephone (str): The telephone number of the contact.
        email (str): The email address of the contact.
        date_added (datetime): The date and time when the contact was created.
        status (ForeignKey): The associated status of the contact.
        user (ForeignKey): The associated users for this contact.

    Meta:
        verbose_name (str): The singular name for this model in the
        admin interface.
        verbose_name_plural (str): The plural name for this model in
        the admin interface.
        ordering (tuple): The default sorting order for instances of
        this model.
    """
    CONTACT_ACTIVE = 'active'
    CONTACT_INACTIVE = 'inactive'

    CONTACTS_STATUSES = (
        (CONTACT_ACTIVE, 'Активный'),
        (CONTACT_INACTIVE, 'Неактивный'),
    )

    telephone = models.CharField(max_length=50, verbose_name='номер телефона')
    email = models.EmailField(max_length=255, verbose_name='почта')
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    status = models.CharField(
        max_length=50,
        choices=CONTACTS_STATUSES,
        verbose_name='статус',
        default=CONTACT_ACTIVE
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    list = models.ForeignKey(
        Lists,
        on_delete=models.SET_NULL,
        related_name='contact_list',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.email}, {self.telephone}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ('date_added',)


class ContactsList(models.Model):
    """
    Represents the relationship between contacts and lists.

    Attributes:
        contact (ForeignKey): The associated contact.
        list (ForeignKey): The associated list.

    Meta:
        verbose_name (str): The singular name for this model in the
        admin interface.
        verbose_name_plural (str): The plural name for this model in
        the admin interface.
        ordering (tuple): The default sorting order for instances of
        this model.
    """
    contact = models.ForeignKey(
        Contacts,
        on_delete=models.CASCADE,
        verbose_name='контакт',
        **NULLABLE
    )
    list = models.ForeignKey(
        Lists,
        on_delete=models.CASCADE,
        verbose_name='список',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.contact} - {self.list}'

    class Meta:
        verbose_name = 'список контакта'
        verbose_name_plural = 'списки контактов'
        ordering = ('list',)
