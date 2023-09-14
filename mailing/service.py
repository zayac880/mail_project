from datetime import date

from crontab import CronTab


def create_cron_jobs(mailing):
    mailing_settings = mailing.setting

    cron = CronTab(
        user=True
    )

    python_executable = '/home/tigranix/.cache/pypoetry/virtualenvs/mailcraft-by-evoq-G3fD8CGT-py3.11/bin/python'
    python_script = 'send_mail'

    job = cron.new(
        comment=f'mailing_{mailing.pk}',
        command=f'{python_executable} -m {python_script} {mailing.pk}',
        pre_comment=True
    )

    minutes, hours, day, month, week_day = '*' * 5

    if mailing_settings.mailing_periods:
        if mailing_settings.mailing_periods == 'daily':
            minutes = mailing_settings.mailing_time.minute
            hours = mailing_settings.mailing_time.hour

        elif mailing_settings.mailing_periods == 'weekly':
            minutes = mailing_settings.mailing_time.minute
            hours = mailing_settings.mailing_time.hour
            week_day = mailing_settings.mailing_week_day_num

        elif mailing_settings.mailing_periods == 'monthly':
            minutes = mailing_settings.mailing_time.minute
            hours = mailing_settings.mailing_time.hour
            day = mailing_settings.start_date.day

    job.setall(f'{minutes} {hours} {day} {month} {week_day}')

    start_date = mailing_settings.start_date
    end_date = mailing_settings.end_date

    if start_date <= date.today() <= end_date:
        job.enable()
    else:
        job.clear()
        cron.remove_all(comment=f'mailing_{mailing.pk}')

        print('Job out of date')

    cron.write()


def remove_cron_jobs(mailing):
    cron = CronTab(
        user=True
    )

    cron.remove_all(comment=f'mailing_{mailing.pk}')
    cron.write()
