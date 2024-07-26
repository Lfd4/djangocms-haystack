from django.db import models
from django.utils.html import strip_tags as _strip_tags
from nh3 import clean


def get_field_value(obj, name):
    # fields may be accessed through relations
    fields = name.split("__")

    name = fields[0]

    try:
        obj._meta.get_field(name)
    except (AttributeError, models.FieldDoesNotExist):
        # we catch attribute error because obj will not always be a model
        # specially when going through multiple relationships.
        value = getattr(obj, name, None) or ""
    else:
        value = getattr(obj, name)

    if len(fields) > 1:
        remaining = "__".join(fields[1:])
        return get_field_value(value, remaining)
    return value


def strip_tags(value):
    """
    Sanitize the potentially dangerous HTML using the Rust ammonia crate
    (through nh3 Python bindings) and strip any excess tags as well.
    This gives us the basic text content to use in the index and preview.
    """

    if isinstance(value, str):
        # remove whitespace
        value = value.strip()

        # remove potentially dangerous content
        partial_strip = clean(value)

        # remove other html tags using native Django util
        value = _strip_tags(partial_strip)
        return value.strip()
    return value
