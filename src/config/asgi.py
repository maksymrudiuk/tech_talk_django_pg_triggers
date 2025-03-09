import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", os.environ.get("__ENV__"))

from configurations.asgi import get_asgi_application

application = get_asgi_application()
