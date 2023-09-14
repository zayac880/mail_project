from django import forms

from frontend.forms import StyleFormMixin
from mailing.models import Mailing, MailingSettings


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = (
            'title',
            'message_title',
            'message_content',
            'contact_list',
        )


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = (
            'mailing',
            'mailing_periods',
            'status',
            'start_date',
            'mailing_time',
            'mailing_week_day_num',
            'end_date',
        )

        widgets = {
            'mailing_time': forms.TimeInput(
                format="%H:%M",
                attrs={
                    'type': 'time',
                }
            ),
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }


class DetailForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = (
            'title',
            'message_title',
            'message_content',
        )
        widgets = {
            'mailing_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }
