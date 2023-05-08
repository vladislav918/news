from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView

from .forms import CommentForm, NewsForms
from .models import Category, Comment, News

User = get_user_model()


def blog_post_like(request, slug):
    post = get_object_or_404(News, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('one_post', args=[slug]))


def get_all_posts(request):
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
        'news': news,
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
        'news': news,
        'categories': categories,
        'category': category,
        'page_obj': page_obj,
    }
    return render(
        request,
        'posts/category.html',
        context=content
    )


class ShowOnePost(DetailView):
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
            return redirect(request.path)

    def get_context_data(self, **kwargs):
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(News, slug=self.kwargs['slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_is_liked': liked,
            'number_of_likes': likes_connected.number_of_likes(),
        })
        return context


@login_required(login_url='/users/register')
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


def error_404(request, exception):
    return render(
        request,
        'error_page/404.html',
        {'path': request.path},
        status=404
    )
