from cms.api import add_plugin, create_page
from cms.models import CMSPlugin, Page, PageContent
from cms.models.placeholdermodel import Placeholder
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib.auth.models import AnonymousUser
from djangocms_haystack.helpers import (
    get_field_value,
    get_haystack_connection_from_request,
    get_plugin_index_data,
    get_request,
    strip_tags,
)


@plugin_pool.register_plugin
class IndexedPlugin(CMSPluginBase):
    model = CMSPlugin
    plugin_content = "<h1>Rendered Plugin Content<h1>"
    render_template = "base.html"

    def render(self, context, instance, placeholder):
        return context


class TestHelpers:
    def test_get_field_values(self):
        class NestedObj:
            def __init__(self):
                self.nested_value = 2

        class Obj:
            def __init__(self):
                self.parent_value = 1
                self.nested = NestedObj()

        obj = Obj()

        # check happy path
        assert get_field_value(obj, "nested__nested_value") == 2
        assert get_field_value(obj, "parent_value") == 1

        # check error path
        assert get_field_value(obj, "nested__unknown_field") == ""

    def test_get_sanitized_data(self):
        poisoned_string = """
            <script>alert('1')</script>
            <div class='test'>
            <img src='' onerror='alert('2')'>
            This is the only text that should show up
            </div>
        """

        assert (
            strip_tags(poisoned_string)
            == "This is the only text that should show up"
        )

    def test_get_request(self, transactional_db):
        req = get_request("en")
        # check language
        assert req.LANGUAGE_CODE == "en"

        # check host
        assert req.META["HTTP_HOST"] == "localhost"

        # check user
        assert isinstance(req.user, AnonymousUser)

    def test_get_plugin_index_data(self, transactional_db):
        instance = CMSPlugin(
            language="en",
            plugin_type="IndexedPlugin",
            placeholder=Placeholder(id=12345),
        )
        instance.cmsplugin_ptr = instance
        instance.pk = 12345

        request = get_request("en")
        assert (
            " ".join(get_plugin_index_data(instance, request))
            == "This is my new project home page"
        )

    def test_get_haystack_connection_from_request(self, transactional_db):
        # en is configured as default language; we expect the "default" index here
        req = get_request("en")
        haystack_index = get_haystack_connection_from_request(req)
        assert haystack_index == "en"

        # de is an additional language; we expect the de index
        req = get_request("de")
        haystack_index = get_haystack_connection_from_request(req)
        assert haystack_index == "default"
