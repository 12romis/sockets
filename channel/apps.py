# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'channel'

    def ready(self):
        import channel.signals