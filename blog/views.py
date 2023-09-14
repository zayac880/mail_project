import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, UpdateView, \
    DetailView, ListView
from pytils.translit import slugify

from blog.forms import PostForm
from blog.models import Posts


class PostSlugifyMixin:
    def form_valid(self, form):
        post = form.save(commit=False)
        slug = slugify(post.title)
        post_objects = Posts.objects
        if post_objects.filter(slug=slug).exists():
            count = 1
            while post_objects.filter(slug=f'{slug}-{count}').exists():
                count += 1
            slug = f'{slug}-{count}'

        post.slug = slug
        post.save()
        return super().form_valid(form)


class PostListView(ListView):

    # TODO:
    #       posts - все посты упорядоченные по дате добавления
    #       featured_posts - 2 самых просматриваемых поста
    #       random_posts - 3 случайных поста за последний месяц
    #       для карусели:
    #       3 рекламных поста
    model = Posts
    context_object_name = 'posts'
    template_name = 'blog/posts_list.html'
    ordering = ('-creation_date',)

    def get_paginate_by(self, queryset):
        if self.request.user.is_authenticated:
            paginate_by = 10
        else:
            paginate_by = 3
        return paginate_by

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            result = queryset.filter(
                user=self.request.user
            )
        else:
            result = queryset.filter(
                is_published=True
            )
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        random.seed(int(current_date.timestamp() * 1000))

        last_month_posts = list(
            Posts.objects.filter(
                creation_date__gte=thirty_days_ago,
                is_published=True
            ).all()
        )

        featured_posts = Posts.objects.order_by('-views_count').filter(
                creation_date__gte=thirty_days_ago,
                is_published=True
            ).all()[:2]
        random_three_posts = random.sample(last_month_posts, 3)
        context.update(
            {
                'featured_posts': featured_posts,
                'random_three_posts': random_three_posts
            }
        )
        return context


class PostDetailView(DetailView):
    model = Posts
    context_object_name = 'post'
    template_name = 'blog/posts_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1

        # TODO: доработать функцию
        #       service.utils.view_counter_email_notification
        self.object.save()

        return self.object


class PostCreateView(
    LoginRequiredMixin, PostSlugifyMixin, CreateView
):
    model = Posts
    template_name = 'blog/posts_form.html'
    slug_url_kwarg = 'slug'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'slug': self.object.slug}
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, PostSlugifyMixin, UpdateView
):
    model = Posts
    template_name = 'blog/posts_form.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'slug': self.object.slug}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog:post_list')
