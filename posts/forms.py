from django import forms
from captcha.fields import CaptchaField

from .models import Comment, News


class NewsForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите название'
                   }
        )
    )
    captcha = CaptchaField()
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'TextArea form-control', 'placeholder': 'Напишите подробнее'})
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-button form-control', 'placeholder': 'Выберите фото'})
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'category']
        labels = {
            'title': 'Название',
            'content': 'Описание',
            'photo': 'Фото',
            'category': 'Категория',
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content',)


class ChangePosts(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите название'
                   }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'TextArea form-control', 'placeholder': 'Напишите подробнее'})
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-button form-control', 'placeholder': 'Выберите фото'})
    )
    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'category']
        labels = {
            'title': 'Название',
            'content': 'Описание',
            'photo': 'Фото',
            'category': 'Категория',
        }