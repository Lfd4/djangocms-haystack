# djangocms-haystack
A ready-to-use basic djangoCMS Page Index based on django-haystack

## What does this package solve?
If you regularly develop djangoCMS sites you may have noticed that there is no built-in way to handle searching for content.

This is a rather common requirement though and because of that we had the issue multiple times when developing sites for our customers. In the past (pre-djangoCMS 4.x era) we would just use the deprecated `aldryn-search` package, fork it & regularly make it compatible with new Django & djangoCMS releases. 

However, this does not work anymore with djangoCMS 4.x since it is just too different. Further, we didn't even needed many of the functionality it provided and so we opted for a custom rewrite of a (as in "one possible") search implementation: this is what is now `djangocms-haystack`.

## Setup
This package heavily relies on the very popular and well supported open source project `django-haystack`. It handles all the necessary tasks of maintaining the search index itself, we just provide the definitions and logic that tells Haystack **what** to index.

### Installation
We strongly recommend using tooling that allows locking your dependencies such as `pipenv`, `poetry` or `uv`. The command therefore depends on your actual tooling but using pip it would be: 

`$ pip install djangocms-haystack`

### Set up Django
Add the following module to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    your other modules here...
    "djangocms_haystack"
]
```

And setup your `HAYSTACK_CONNECTIONS` according to your djangoCMS language setup. We recommend using a standalone connection name for each language and this is also what the index logic ships with. A setup could look like this:

```python
LANGUAGE_CODE = "de"
CMS_LANGUAGES = PARLER_LANGUAGES = {
    1: [
        {
            "code": "de",
            "name": _("de"),
            "redirect_on_fallback": False,
            "public": True,
            "hide_untranslated": True,
        },
        {
            "code": "en",
            "name": _("en"),
            "redirect_on_fallback": False,
            "public": True,
            "hide_untranslated": True,
        },
        {
            "code": "fr",
            "name": _("fr"),
            "redirect_on_fallback": False,
            "public": True,
            "hide_untranslated": True,
        },
    ],
    "default": {
        "fallbacks": ["en", "de"],
        "redirect_on_fallback": False,
        "public": True,
        "hide_untranslated": True,
    },
}

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "search_index", "de"),
    },
    "en": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "search_index", "en"),
    },
    "fr": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "search_index", "fr"),
    },
}
```

Your `LANGUAGE_CODE` is the default language of your setup. Django will always fall back to it when other options don't yield results or are not present. This is according to the [official Django documentation](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/#how-django-discovers-language-preference).

Assuming this behaviour we also use it as the default index, so we only need to add a haystack connection for th remaining languages. If you have a single language setup, you can skip them and only use the `default` connection.

If you want to use other backends than `whoosh` you need to install the necessary adapters yourself & change the `ENGINE` according to the official [Django Haystack Docs](https://django-haystack.readthedocs.io/en/master/backend_support.html)

## Index Lifecycle
### Creating the index
Create the initial index using the following management command:

`$ python manage.py rebuild_index`

This will create the initial index and all the necessary files/indexes in your configured backend.

### Update the index
To update your index you can use the folling command:

`$ python manage.py update_index`

This will update the index *without removing stale data*.
If you want to remove stale data (e.g. if pages were deleted inside the CMS), use the `--remove`:

`$ python manage.py update_index --remove`

## Extend the index beyond CMS pages 
To index your own custom models you can extend the base class of our index and implement the necessary methods for your model as you need them. 

Let's have a look at an index that handles a custom built `News` model:

```python
from djangocms_haystack.base import DjangoCMSSearchIndexBase, indexes
from my_news_app.models import News


class NewsIndex(DjangoCMSSearchIndexBase, indexes.Indexable):
    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_title(self, instance):
        return instance.title

    def get_description(self, instance):
        return instance.teaser or ""

    def get_model(self):
        return News

    def get_index_queryset(self, language):
        return News.objects.filter(
            translations__language_code=language,
            published=True,
        )

    def should_update(self, instance, **kwargs):
        return True
```

As you can see, it exposes some very sane defaults for you to implement and you'll then get your model indexed just like the CMS pages. Notice that you need to implement all custom utility methods on them, such as `get_absolute_url()`.

## Support
If you need support, have some ideas about features or just need to ask for something, please feel free to open an issue.