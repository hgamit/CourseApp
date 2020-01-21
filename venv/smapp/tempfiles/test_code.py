from django.test.utils import setup_test_environment
setup_test_environment()
from django.test import Client
client = Client()



from django.urls import reverse, resolve
from django.urls import resolve
from django.test import TestCase
from maintain.views import home, cou_detail
from maintain.models import course