from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .forms import NewsForm
from .models import Post
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-created_at')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_1.html'
    context_object_name = 'news'


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Новости
class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_form.html'

    def form_valid(self, form):
        form.instance.news_choice_article = 'NE'  # Устанавливаем тип "Новость"
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_form.html'

    def get_queryset(self):
        return Post.objects.filter(news_choice_article='NE')  # Только новости


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(news_choice_article='NE')  # Только новости


# Статьи
class ArticleList(ListView):
    model = Post
    template_name = 'articles_list.html'  # Шаблон для списка статей
    context_object_name = 'articles'
    paginate_by = 10
    ordering = '-created_at'

    def get_queryset(self):
        return Post.objects.filter(news_choice_article='AR')


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_form.html'

    def form_valid(self, form):
        form.instance.news_choice_article = 'AR'  # Устанавливаем тип "Статья"
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_form.html'

    def get_queryset(self):
        return Post.objects.filter(news_choice_article='AR')  # Только статьи


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(news_choice_article='AR')

