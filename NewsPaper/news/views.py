from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-created_at')
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("News in context:", context['news'])  # Проверьте, что здесь выводятся ожидаемые данные
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_1.html'
    context_object_name = 'news'