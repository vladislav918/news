from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from users.models import User


class News(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    content = models.TextField(verbose_name='Контент')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    photo = models.ImageField(
        upload_to='img/',
        verbose_name='Фото',
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликован'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        default='',
        null=False
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('one_post', args=[self.slug])


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey('News', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user
