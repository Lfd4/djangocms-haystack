from django.conf import settings

from .settings import SETTINGS as DEFAULT_SETTINGS


# TODO: I could add custom settings in here,
# maybe useful for later
def pytest_configure():
    settings.configure(**DEFAULT_SETTINGS)
