from django.test import TestCase
from django.urls import reverse
from ..models import course, classroom
import datetime

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        
        course.objects.create(course_name='Django', course_description='Learn Django.', course_type='', course_notes='', course_last_updated=datetime.datetime.now() , course_clsroom_id=1)
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))