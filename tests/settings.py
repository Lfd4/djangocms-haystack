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
    "INSTALLED_APPS": [
        "djangocms_admin_style",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "haystack",
        "djangocms_haystack",
        "cms",
        "menus",
        "sekizai",
        "treebeard",
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
    "CMS_TEMPLATES": (
        ("fullwidth.html", "Fullwidth"),
        ("page.html", "Normal page"),
        ("test.html", "Normal page2"),
    ),
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
    # 'TEMPLATE_LOADERS': ('aldryn_search.tests.FakeTemplateLoader',),
    "HAYSTACK_CONNECTIONS": HAYSTACK_CONNECTIONS,
    "CMS_PERMISSION": True,
    "CMS_PLACEHOLDER_CONF": {
        "content": {},
    },
}

SETTINGS = {**HELPER_SETTINGS}
