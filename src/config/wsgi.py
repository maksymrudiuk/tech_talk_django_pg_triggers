import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", os.environ.get("__ENV__"))

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
