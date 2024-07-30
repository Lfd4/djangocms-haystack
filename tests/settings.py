HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "whoosh_index/de",
        "TIMEOUT": 60 * 5,
        "INCLUDE_SPELLING": True,
    },
    "en": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "whoosh_index/en",
        "TIMEOUT": 60 * 5,
        "INCLUDE_SPELLING": True,
    },
}

HELPER_SETTINGS = {
    "DEBUG": True,
    "TEST_RUNNER": "app_helper.pytest_runner.PytestTestRunner",
    "INSTALLED_APPS": [
        "haystack",
        "djangocms_haystack",
    ],
    "MIDDLEWARE": [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "cms.middleware.user.CurrentUserMiddleware",
        "cms.middleware.page.CurrentPageMiddleware",
        "cms.middleware.toolbar.ToolbarMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "cms.middleware.language.LanguageCookieMiddleware",
    ],
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.i18n",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "sekizai.context_processors.sekizai",
                    "cms.context_processors.cms_settings",
                ],
            },
        },
    ],
    "ALLOWED_HOSTS": ["localhost"],
    "CMS_LANGUAGES": {
        1: [
            {"code": "de", "name": "Deutsch"},
            {"code": "en", "name": "English"},
        ]
    },
    "LANGUAGES": (
        ("de", "Deutsch"),
        ("en", "English"),
    ),
    "LANGUAGE_CODE": "de",
    "HAYSTACK_CONNECTIONS": HAYSTACK_CONNECTIONS,
    "CMS_PERMISSION": True,
    "CMS_PLACEHOLDER_CONF": {
        "content": {},
    },
    "CMS_CONFIRM_VERSION4": True,
}
