from django import forms
from .models import News, Comment


class NewsForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    content = forms.CharField(label="Описание", widget=forms.Textarea(attrs={"class": "TextArea form-control"}))
    photo = forms.ImageField(label="Фото", widget=forms.FileInput(attrs={'class': 'custom-button form-control'}))

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'category']
        labels = {
            'title': "Название",
            "content": "Описание",
            "photo": "Фото",
            "category": "Категория",
        }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content',)
