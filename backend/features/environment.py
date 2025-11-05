"""
Behave environment configuration.
"""
import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spontime.settings')


def before_all(context):
    django.setup()


def before_scenario(context, scenario):
    call_command('flush', '--noinput')
