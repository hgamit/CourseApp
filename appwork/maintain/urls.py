from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('course_new/', views.course_new, name='course_new'),
    path('<int:course_id>/', views.cou_detail, name='cou_detail')
]