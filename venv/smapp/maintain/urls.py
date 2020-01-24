from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('<int:course_id>/', views.course_topics, name='course_topics'),
    path('<int:course_id>/topics/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('<int:course_id>/topics/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
    path('<int:course_id>/topics/<int:topic_id>/posts/<int:post_id>/edit/', views.update_post, name='edit_post'),
    path('<int:course_id>/course_update/', views.course_update, name='course_update'),
    path('<int:course_id>/', views.cou_detail, name='cou_detail'),
    path('<int:course_id>/classes/<int:class_id>/classroom', views.classroom_detail, name='classroom_detail')
]