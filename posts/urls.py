from django.urls import reverse, path
from . import views


urlpatterns = [
    path('make_post', views.make_post, name='make post'),
    path('home', views.homepage, name='home page'),
    path('view_post/<int:post_id>', views.view_post, name='view post page'),
]