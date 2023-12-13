from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from app.consumers import *
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project_veriosn1.settings')
application=get_asgi_application()
websocket_urlpatterns=[
    path("ws/app/",TestConsumer)
    ]
application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
