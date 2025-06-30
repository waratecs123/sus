from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import NewsForm
from .models import Post
from .filters import NewsFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NE').order_by('-created_at')
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return Post.objects.filter(post_type='NE')


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NE').order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'NE'
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_form.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='NE', author=self.request.user.author)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NE', author=self.request.user.author)


class ArticleList(ListView):
    model = Post
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='AR').order_by('-created_at')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = NewsForm
    model = Post
    template_name = 'article_form.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.post_type = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'article_form.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='AR', author=self.request.user.author)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        if hasattr(self.request.user, 'author'):
            return Post.objects.filter(
                post_type='AR',
                author=self.request.user.author
            )
        return Post.objects.none()


@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')
    request.user.groups.add(authors_group)
    messages.success(request, 'Поздравляем! Теперь вы автор!')
    return redirect('news_list')