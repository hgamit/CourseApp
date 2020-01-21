from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home_boards'),
    path('<int:pk>', views.board_topics, name='board_topics'),
]