from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item, List

# Run with 'python manage.py test lists'

