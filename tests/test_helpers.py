from djangocms_haystack.helpers import get_field_value


class TestHelpers:
    def test_get_field_values(self, settings):
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
