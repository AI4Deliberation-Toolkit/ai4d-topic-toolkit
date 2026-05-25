"""
ASGI config for ai4d_topic_toolkit project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4d_topic_toolkit.settings.settings')

application = get_asgi_application()
