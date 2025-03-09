from django.apps import AppConfig
from django.utils.translation import gettext_noop as _


class Config(AppConfig):
    label = "sandbox"
    name = "apps.sandbox"
    verbose_name = _("Sandbox")
