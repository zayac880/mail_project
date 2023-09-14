from django import forms

from blog.models import Posts
from frontend.forms import StyleFormMixin

PROHIBITED_WORDS = []


def validate_prohibited_words(clean_data):
    for word in PROHIBITED_WORDS:
        if word.lower() in clean_data.lower():
            raise forms.ValidationError(
                'Вы использовали одно из запрещённых слов: \n'
                f'{", ".join(PROHIBITED_WORDS)}'
            )


class PostForm(StyleFormMixin, forms.ModelForm):

    def clean_title(self):
        clean_data = self.cleaned_data['title']
        validate_prohibited_words(clean_data)
        return clean_data

    def clean_content(self):
        clean_data = self.cleaned_data['content']
        validate_prohibited_words(clean_data)
        return clean_data

    class Meta:
        model = Posts
        fields = ('title', 'content', 'image', 'is_published')
