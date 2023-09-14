from datetime import datetime


def save_picture(instance, filename):
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name
    my_date = str(datetime.now().isoformat())

    picture_name = "".join(
        [
            "".join(filename.split('.')[:-1]),
            my_date,
            ".",
            filename.split('.')[-1]
        ]
    )
    return f"{app_name}/{model_name}/{instance.pk}/{instance.pk}_{picture_name}"


def view_counter_email_notification(views_count, title):
    if views_count == 100:
        subject = f'Поздравляем!'
        message = f'<p>Пост {title} достиг ' \
                  f'отметки в 100 просмотров</p>'
        email = 'mr.saatchyan@yandex.com'

        send_mail(

            subject=subject,
            from_email=None,
            recipient_list=[email],
            message=message
        )
