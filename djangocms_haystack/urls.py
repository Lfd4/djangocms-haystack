from django.urls import path

from djangocms_haystack.views import SearchView

urlpatterns = [path("", SearchView.as_view())]
