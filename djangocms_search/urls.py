from django.urls import path

from djangocms_search.views import SearchView

urlpatterns = [path("", SearchView.as_view())]
