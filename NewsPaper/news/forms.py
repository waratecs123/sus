from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class NewsForm(forms.ModelForm):
    description = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Текст статьи/новости',
        required=True
    )

    class Meta:
        model = Post
        fields = ['heading', 'author', 'news_choice_article', 'categories', 'text_n_ar']
        widgets = {
            'news_choice_article': forms.RadioSelect,
            'categories': forms.CheckboxSelectMultiple,
        }
        labels = {
            'heading': 'Заголовок',
            'author': 'Автор',
            'news_choice_article': 'Тип публикации',
            'categories': 'Категории',
            'text_n_ar': 'Основной текст',
        }

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("heading")
        author = cleaned_data.get("author")

        if heading and author and str(author) in heading:
            raise ValidationError(
                "Имя автора не должно содержаться в заголовке."
            )

        return cleaned_data