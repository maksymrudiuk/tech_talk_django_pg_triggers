from configurations import Configuration

from .common import Settings


class Local(Settings, Configuration):
    # INSTANCE CONFIGURATION
    # =======================================================================
    DIST = True
    DEBUG = True

    # SESSION CONFIGURATION
    # =======================================================================
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

    # EMAIL CONFIGURATION
    # =======================================================================
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # CACHING
    # =======================================================================
    @property
    def CACHES(self):
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": self._REDIS_NETLOC,
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    "PARSER_CLASS": "redis.connection.DefaultParser",
                    "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                    "SERIALIZER": "django_redis.serializers.pickle.PickleSerializer",
                    "IGNORE_EXCEPTIONS": True,
                },
            }
        }

    # LOGGING CONFIGURATION
    # =======================================================================
    @property
    def LOGGING(self):
        level = "DEBUG"
        return self._update_logging(
            super().LOGGING, level=level, formater="verbose", handler="console"
        )

    @property
    def TEMPLATES(self):
        TEMPLATES = super().TEMPLATES
        TEMPLATES[0]["OPTIONS"].update({"debug": self.DEBUG})
        return TEMPLATES
