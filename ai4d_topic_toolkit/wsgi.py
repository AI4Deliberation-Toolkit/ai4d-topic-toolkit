"""
WSGI config for ai4d_topic_toolkit project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4d_topic_toolkit.settings.settings')

application = get_wsgi_application()
