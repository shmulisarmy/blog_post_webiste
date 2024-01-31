from django.urls import reverse, path
from . import views


urlpatterns = [
    path('make_post', views.make_post, name='make post'),
    path('home', views.homepage, name='home page'),
    path('', views.homepage, name='home page'),
    path('view_post/<int:post_id>', views.view_post, name='view post'),
    path('delete comment/<int:comment_id>', views.delete_comment, name='delete comment'),
    path('delete post/<int:post_id>', views.delete_post, name='delete post'),
]