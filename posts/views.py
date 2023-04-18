from django.shortcuts import render, redirect
from .models import News, Category, Comment
from django.core.paginator import Paginator
from .forms import CommentForm, NewsForms
from django.views.generic import DetailView


def all_posts(request):
    search_list = request.GET.get('search', '')
    if search_list:
        news = News.objects.filter(
            title__icontains=search_list
        )
    else:
        news = News.objects.all()

    categories = Category.objects.all()
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {
        'blog': news,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(
        request,
        'posts/home.html',
        context=content
    )


def get_category(request, category_id):
    news = News.objects.filter(
        category_id=category_id
    )
    categories = Category.objects.all()
    category = Category.objects.get(
        pk=category_id
    )
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {
        'blog': news,
        'categories': categories,
        'category': category,
        'page_obj': page_obj,
    }
    return render(
        request,
        'posts/category.html',
        context=content
    )


class Show_one_post(DetailView):
    template_name = 'posts/one_news.html'
    model = News

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect('home')

    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context


def add_post(request):
    if request.method == 'POST':
        form = NewsForms(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    else:
        form = NewsForms
    return render(
        request,
        'posts/new_news.html',
        context={'form': form}
    )
