# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url,include
from view.views import home
# Create your view here.
urlpatterns = [
    url(r'^$',home, name='home')
]
