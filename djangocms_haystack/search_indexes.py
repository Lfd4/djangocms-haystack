from cms.models import PageContent
from django.db.models import Q
from haystack import indexes

from djangocms_haystack.base import DjangoCMSSearchIndexBase


class PageContentIndex(DjangoCMSSearchIndexBase, indexes.Indexable):
    def get_url(self, instance):
        return instance.page.get_absolute_url()

    def get_title(self, instance):
        return instance.title

    def get_description(self, instance):
        return instance.meta_description or ""

    def get_model(self):
        return PageContent

    def get_index_queryset(self, language):
        return PageContent.objects.filter(
            Q(redirect__exact="") | Q(redirect__isnull=True),
            versions__state="published",
            language=language,
        ).distinct()

    def should_update(self, instance, **kwargs):
        # Instantly update the index on pagecontent changes
        return True
