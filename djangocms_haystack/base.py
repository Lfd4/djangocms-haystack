from typing import Optional

from cms.models import CMSPlugin, Placeholder
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils import translation
from haystack import indexes

from djangocms_haystack.helpers import get_plugin_index_data, get_request


class DjangoCMSSearchIndexBase(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=False)
    language = indexes.CharField()
    description = indexes.CharField(indexed=False, stored=True, null=True)
    url = indexes.CharField(stored=True, indexed=False)
    title = indexes.CharField(stored=True, indexed=False)

    login_required: bool = False
    index_title: bool = True

    # TODO: obey these fields when building the index
    # and build some kind of discovery method for their prepare functions
    fields: list[str] = ["description", "title"]
    use_placeholders: bool = True

    def get_request_instance(self, language: str) -> WSGIRequest:
        return get_request(language)

    def get_language(self) -> Optional[str]:
        index_connection = self._haystack_connection_alias

        """
        The 'default' haystack connection alias
        is used for the configured default language
        """
        if index_connection == "default":
            return settings.LANGUAGE_CODE

        """
        If connection_alias is also a key inside
        the configured languages, use it instead
        """
        if index_connection in [lang[0] for lang in settings.LANGUAGES]:
            return index_connection

        """
        Block indexing of content to not pollute index
        """
        return None

    def index_queryset(self, using: Optional[str] = None) -> models.QuerySet:
        self._haystack_connection_alias = using
        language = self.get_language()
        if not language:
            return self.get_model().none()

        return self.get_index_queryset(language)

    def get_model(self) -> models.Model:
        raise NotImplementedError

    def get_url(self, instance: models.Model) -> str:
        raise NotImplementedError

    def get_title(self, instance: models.Model) -> str:
        raise NotImplementedError

    def get_description(self, instance: models.Model) -> str:
        raise NotImplementedError

    def get_index_queryset(self, language: str) -> models.QuerySet:
        raise NotImplementedError

    def get_plugin_queryset(self, language: str) -> models.QuerySet[CMSPlugin]:
        return CMSPlugin.objects.filter(language=language)

    def get_plugin_search_text(
        self, base_plugin: CMSPlugin, request: WSGIRequest
    ) -> str:
        plugin_content = get_plugin_index_data(base_plugin, request)

        # filter empty items
        filtered_plugin_content = filter(None, plugin_content)

        # concatenate the final index string for the plugin
        return " ".join(filtered_plugin_content)

    def get_placeholders(
        self, instance: models.Model, *args: list, **kwargs: dict
    ) -> models.QuerySet[Placeholder]:
        if instance.placeholders:
            return instance.placeholders.filter(*args, **kwargs)
        return []

    def get_search_data(
        self, instance: models.Model, language: str, request: WSGIRequest
    ) -> str:
        placeholders = self.get_placeholders(instance)
        if not placeholders:
            return ""

        plugins = self.get_plugin_queryset(language).filter(
            placeholder__in=placeholders
        )
        content = []

        for base_plugin in plugins:
            plugin_text_content = self.get_plugin_search_text(base_plugin, request)
            content.append(plugin_text_content)

        if getattr(instance, "page", None):
            page_meta_description = instance.page.get_meta_description(
                fallback=False, language=language
            )

            if page_meta_description:
                content.append(page_meta_description)

            page_meta_keywords = getattr(instance.page, "get_meta_keywords", None)

            if callable(page_meta_keywords):
                content.append(page_meta_keywords())

        return " ".join(content)

    def prepare_fields(
        self, instance: models.Model, language: str, request: WSGIRequest
    ) -> None:
        self.prepared_data["language"] = language
        self.prepared_data["url"] = self.get_url(instance)
        self.prepared_data["title"] = self.get_title(instance)
        self.prepared_data["description"] = self.get_description(instance)
        self.prepared_data["text"] = (
            f"{self.prepared_data['title']} {self.prepared_data['text']}"
        )

    def prepare(self, instance: models.Model) -> dict:
        current_language = self.get_language()
        if not current_language:
            return super().prepare(instance)

        with translation.override(current_language):
            request = self.get_request_instance(current_language)
            self.prepared_data = super().prepare(instance)
            self.prepared_data["text"] = self.get_search_data(
                instance, current_language, request
            )
            self.prepare_fields(instance, current_language, request)
            return self.prepared_data
