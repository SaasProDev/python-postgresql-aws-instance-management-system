from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _('api')

    def ready(self):
        import core.signals  # noqa

