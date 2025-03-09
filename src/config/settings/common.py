import os
import socket
import sys
import urllib.parse


class Settings:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Run environment variables check before start """
        red, bold, end = "\033[91m", "\033[1m", "\033[0m"

        if not os.environ.get("__ENV__"):
            info = "__ENV__ variable is not defined."
            sys.stdout.write("{}{}{}{}\n".format(red, bold, info, end))
            sys.exit(-1)

        environment = self._get_env_vars()

        def rs(path):
            with open(path, "r") as f:
                return f.read().replace("\n", "").strip()

        mv = []

        for e in environment:
            key = e
            val = os.environ.get(key)
            if not val:
                key = f"{e}_FILE"
                val = os.environ.get(key)
                if val:
                    val = rs(os.environ.get(key))

            if not val:
                mv.append(key)
            else:
                setattr(self, "_%s" % e, val)

        if mv:
            msg_map = ""
            for e in mv:
                msg_map += "{}: {},\n ".format(e, os.environ.get(e))
            info = (
                "Environment configuration error. Some of next "
                + "variables is not defined:\n {}."
            ).format(msg_map)

            sys.stdout.write("{}{}{}{}\n".format(red, bold, info, end))
            sys.exit(-1)

    def _get_env_vars(self):
        return [
            "SSL",
            "DOMAIN",
            "SECRET_KEY",
            "POSTGRES_NETLOC",
            "REDIS_NETLOC",
            "RABBIT_NETLOC",
            "MEDIA_URL",
            "STATIC_URL",
        ]

    # INSTANCE CONFIGURATION
    # =======================================================================
    DEBUG = False
    DIST = False

    SITE_ID = 1

    ASGI_APPLICATION = "config.asgi.application"
    WSGI_APPLICATION = "config.wsgi.application"

    @property
    def SECRET_KEY(self):
        return self._SECRET_KEY

    # URL CONFIGURATION
    # =======================================================================
    ROOT_URLCONF = "config.urls"

    @property
    def USE_HTTPS(self):
        return self._SSL == "on"

    @property
    def DOMAIN(self):
        return self._DOMAIN

    @property
    def DOMAIN_NAME(self):
        return self.DOMAIN

    @property
    def PROTO(self):
        return "http" if not self.USE_HTTPS else "https"

    @property
    def DOMAIN_URL(self):
        return f"{self.PROTO}://{self.DOMAIN}"

    @property
    def FRONTEND_URL(self):
        return self.DOMAIN_URL

    # HOST CONFIGURATION
    # =======================================================================
    @property
    def ALLOWED_HOSTS(self):
        return [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "kubernetes.docker.internal",
            self.DOMAIN,
        ]

    @property
    def INTERNAL_IPS(self):
        return [
            "localhost",
            "127.0.0.1",
            "10.0.2.2",
            self.DOMAIN,
            socket.gethostbyname(socket.gethostname())[:-1] + "1",
        ]

    # PATH CONFIGURATION
    # =======================================================================
    _FILE_PATH = os.path.dirname(__file__)
    _TMP_DIR_NAME = "tmp"
    _LOCALE_DIR_NAME = "locale"
    _FIXTURE_DIR_NAME = "fixtures"
    _PUBLIC_DIR_NAME = "public"

    CONFIG_PATH = os.path.abspath(os.path.join(_FILE_PATH, os.pardir))
    PROJECT_PATH = os.path.abspath(os.path.join(CONFIG_PATH, os.pardir))
    TEMP_PATH = os.path.abspath(os.path.join(PROJECT_PATH, _TMP_DIR_NAME))

    PUBLIC_ROOT = os.path.join(PROJECT_PATH, _PUBLIC_DIR_NAME)

    LOCALE_PATHS = (os.path.join(PROJECT_PATH, _LOCALE_DIR_NAME),)
    FIXTURE_DIRS = (os.path.abspath(os.path.join(PROJECT_PATH, _FIXTURE_DIR_NAME)),)

    # MIDDLEWARE CONFIGURATION
    # =======================================================================
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # DATABASE CONFIGURATION
    # =======================================================================
    @property
    def DATABASES(self):
        engine = "django.db.backends.postgresql"
        config = urllib.parse.urlparse(self._POSTGRES_NETLOC)
        return {
            "default": {
                "ENGINE": engine,
                "NAME": config.path[1:],
                "USER": config.username,
                "PASSWORD": config.password,
                "HOST": config.hostname,
                "PORT": config.port,
                "ATOMIC_REQUESTS": True,
                "CONN_MAX_AGE": 0,  # closing the database connection at
                # the end of each request
            }
        }

    # CACHING
    # =======================================================================
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "",
        }
    }

    # GENERAL CONFIGURATION
    # =======================================================================

    # I18N CONFIGURATION
    # =======================================================================
    USE_TZ = True
    TIME_ZONE = "UTC"

    USE_I18N = True
    USE_L10N = True
    LANGUAGE_CODE = "en"
    LANGUAGES = (("en", "English"),)

    # TEMPLATE CONFIGURATION
    # =======================================================================
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
            "DIRS": [],
            "OPTIONS": {
                "debug": DEBUG,
                "loaders": [
                    (
                        "django.template.loaders.cached.Loader",
                        [
                            "django.template.loaders.filesystem.Loader",
                            "django.template.loaders.app_directories.Loader",
                        ],
                    )
                ],
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                ],
                "libraries": {},
                "builtins": [
                    "django.templatetags.i18n",
                    "django.templatetags.l10n",
                    "django.templatetags.static",
                ],
            },
        }
    ]

    @property
    def STATIC_URL(self):
        return self._STATIC_URL

    STATIC_ROOT = os.path.join(PUBLIC_ROOT, "static")
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )
    STATICFILES_DIRS = (os.path.join(PROJECT_PATH, "static"),)

    @property
    def MEDIA_URL(self):
        return self._MEDIA_URL

    MEDIA_ROOT = os.path.join(PUBLIC_ROOT, "media")

    # PASSWORD VALIDATION
    # =======================================================================
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # APP CONFIGURATION
    # =======================================================================

    # FRAMEWORK CONFIGURATION
    # -----------------------------------------------------------------------
    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.messages",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "django.contrib.admin",
        "configurations",
        "pgtrigger",
        "apps.sandbox.apps.Config",
    ]

    MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # LOGGING CONFIGURATION
    # =======================================================================
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
            },
            "verbose": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
            },
            "file": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
            },
        },
        "filters": {
            "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
            "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "stderr": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stderr,
            },
            "stdout": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
            "null": {"class": "logging.NullHandler"},
        },
        "loggers": {
            "django": {
                "level": "ERROR",
                "handlers": ["stderr"],
                "propagate": False,
            },
            "django.request": {
                "handlers": ["stderr"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.template": {
                "handlers": ["null"],
                "propagate": False,
            },
            "django.channels": {
                "handlers": ["stderr"],
                "level": "INFO",
                "propagate": False,
            },
            "django.utils.autoreload": {
                "level": "ERROR",
                "propagate": False,
            },
            "apps": {
                "handlers": ["stderr"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {"handlers": ["stderr"], "level": "ERROR", "propagate": False},
    }

    def _update_logging(self, config, level=None, formater=None, handler=None):
        for logger in config["loggers"]:
            if logger in ("django.utils.autoreload"):
                continue
            if handler:
                if not isinstance(handler, list):
                    handler = [handler]
                if "null" not in config["loggers"][logger]["handlers"]:
                    config["loggers"][logger]["handlers"] = handler

            config["loggers"][logger]["level"] = level

        config["root"]["handlers"] = handler
        config["root"]["level"] = level

        for handler in config["handlers"]:
            if handler == "file":
                continue
            if formater:
                config["handlers"][handler]["formatter"] = formater

        return config
