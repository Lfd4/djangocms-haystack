from typing import Optional

from cms.models import CMSPlugin
from cms.plugin_rendering import ContentRenderer
from cms.toolbar.toolbar import CMSToolbar
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.template import Engine, RequestContext
from django.test import RequestFactory
from django.utils import translation
from django.utils.text import smart_split

from djangocms_search.utils import (
    get_field_value,
    strip_tags,
)


def get_sanitized_text(data):
    stripped = strip_tags(data)
    return smart_split(stripped)


def get_plugin_index_data(base_plugin: CMSPlugin, request: WSGIRequest):
    rendered_plugin_content = []
    instance, plugin_type = base_plugin.get_plugin_instance()

    if instance is None:
        return rendered_plugin_content

    # Many django CMS extensions (and the CMS itself)
    # set their search_fields explicitly like this,
    # so this needs to stay included to ensure compatibility.
    search_fields = getattr(instance, "search_fields", [])

    if hasattr(instance, "search_fulltext"):
        # check current child instance of CMSPlugin
        search_contents = instance.search_fulltext
    elif hasattr(base_plugin, "search_fulltext"):
        # check default for CMSPlugin
        search_contents = base_plugin.search_fulltext
    elif hasattr(plugin_type, "search_fulltext"):
        # check CMSPluginBase
        search_contents = plugin_type.search_fulltext
    else:
        # only search full content when no explicit
        # search_fields are defined
        search_contents = not bool(search_fields)

    if search_contents:
        context = RequestContext(request)
        updates = {}
        engine = Engine.get_default()

        for processor in engine.template_context_processors:
            updates.update(processor(context.request))
        context.dicts[context._processors_index] = updates

        renderer = ContentRenderer(request)
        plugin_contents = renderer.render_plugin(instance, context)

        if plugin_contents:
            rendered_plugin_content = get_sanitized_text(plugin_contents)
    else:
        values = (get_field_value(instance, field) for field in search_fields)
        for value in values:
            cleaned_bits = get_sanitized_text(value or "")
            rendered_plugin_content.extend(cleaned_bits)
    return rendered_plugin_content


def get_request(language: Optional[str] = None) -> WSGIRequest:
    """Fake WSGIRequest for cms plugin rendering"""
    request = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0]).get("/")
    request.LANGUAGE_CODE = language
    request.user = AnonymousUser()

    # some apps require a CMSToolbar instance to be present,
    # e.g. cms_menus. So instantiate one and add it to the request.
    request.toolbar = CMSToolbar(request)
    return request


def get_haystack_connection_from_request(request: WSGIRequest):
    language = translation.get_language_from_request(request, check_path=True)
    if language == settings.LANGUAGE_CODE:
        return "default"

    if language in [lang[0] for lang in settings.LANGUAGES]:
        return language

    # use default language for search if selected lang isn't configured
    return "default"
