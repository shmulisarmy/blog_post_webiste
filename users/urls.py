from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signup, name='sign up'),
    path('login', views.login, name='log in'),
    path('logout', views.logout, name='log out'),
    path('profilepage/<str:user>', views.profilepage, name='profile page'),
]