from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostDeleteView, PostUpdateView, PostCreateView, \
    PostDetailView, PostListView

app_name = BlogConfig.name

urlpatterns = [
    path(
        'posts/list/',
        PostListView.as_view(),
        name='post_list'
    ),
    path(
        'posts/view/<slug:slug>',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/update/<slug:slug>',
        PostUpdateView.as_view(),
        name='update_post'
    ),
    path(
        'posts/delete/<slug:slug>',
        PostDeleteView.as_view(),
        name='delete_post'
    )
]
