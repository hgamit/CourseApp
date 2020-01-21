from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, cou_detail, course_update
from .models import course, classroom
import datetime
#from django.test.utils import setup_test_environment, teardown_test_environment

class HomeTests(TestCase):
    def setUp(self):
        classroom_obj = classroom.objects.create(class_name='OSS313', class_description='OSS313', class_type='Lecture', class_location='O\'Shaughnessy Science Hall (OSS)', class_capacity=30, class_last_updated=datetime.datetime.now())
        self.course = course.objects.create(course_name='Django', course_description='Learn Django.', course_type='', course_notes='', course_last_updated=datetime.datetime.now(), course_clsroom = classroom_obj)
        #self.course.course_clsroom = classroom_obj
        url = reverse('courses')
        self.response = self.client.get(url)
    
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/maintain/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_cou_detail_page(self):
        cou_detail_url = reverse('cou_detail', kwargs={'course_id': self.course.id})
        self.assertContains(self.response, 'href="{0}"'.format(cou_detail_url))


class CourseTests(TestCase):
    def setUp(self):
        classroom_obj = classroom.objects.create(class_name='OSS313', class_description='OSS313', class_type='Lecture', class_location='O\'Shaughnessy Science Hall (OSS)', class_capacity=30, class_last_updated=datetime.datetime.now())
        course_obj = course.objects.create(course_name='Django', course_description='Learn Django.', course_type='', course_notes='', course_last_updated=datetime.datetime.now() , course_clsroom = classroom_obj)

    def test_cou_detail_view_success_status_code(self):
        url = reverse('cou_detail', kwargs={'course_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_cou_detail_view_not_found_status_code(self):
        url = reverse('cou_detail', kwargs={'course_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_cou_url_resolves_cou_detail_view(self):
        view = resolve('/maintain/1/')
        self.assertEquals(view.func, cou_detail)

    def test_cou_detail_view_contains_link_back_to_homepage(self):
        cou_detail_url = reverse('cou_detail', kwargs={'course_id': 1})
        response = self.client.get(cou_detail_url)
        homepage_url = reverse('courses')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewCourseUpdateTests(TestCase):
    def setUp(self):
        classroom_obj = classroom.objects.create(class_name='OSS313', class_description='OSS313', class_type='Lecture', class_location='O\'Shaughnessy Science Hall (OSS)', class_capacity=30, class_last_updated=datetime.datetime.now())
        course_obj = course.objects.create(course_name='Django', course_description='Learn Django.', course_type='', course_notes='', course_last_updated=datetime.datetime.now() , course_clsroom = classroom_obj)

    def test_new_course_view_success_status_code(self):
        url = reverse('course_update')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_course_url_resolves_new_course_view(self):
        view = resolve('/maintain/course_update/')
        self.assertEquals(view.func, course_update)

    def test_new_course_view_contains_link_back_to_courses_view(self):
        new_course_url = reverse('course_update')
        courses_url = reverse('courses')
        response = self.client.get(new_course_url)
        self.assertContains(response, 'href="{0}"'.format(courses_url))