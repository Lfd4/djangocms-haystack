from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from djangocms_haystack.helpers import get_haystack_connection_from_request


class SearchView(FormMixin, ListView):
    load_all = False

    form_class = ModelSearchForm

    paginate_by = getattr(settings, "djangocms_haystack_PAGINATION", 10)
    paginator_class = Paginator

    template_name = "djangocms_haystack/search.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["load_all"] = self.load_all
        kwargs["searchqueryset"] = self.get_search_queryset()
        kwargs["data"] = self.request.GET
        return kwargs

    def get_query(self, form):
        # Fallback to empty search string when user query is invalid.
        if form.is_valid():
            return form.cleaned_data["q"]

        return ""

    def paginate_queryset(self, queryset, page_size):
        page_query_param = self.page_kwarg
        page_number = self.request.GET.get(page_query_param, 1)

        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        if paginator.num_pages < page_number:
            page_number = paginator.num_pages

        page = paginator.get_page(page_number)
        return (paginator, page, page.object_list, page.has_other_pages())

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Only show results with login_required=True to users
        # who are authenticated.
        queryset = self.form.search()
        if not self.request.user.is_authenticated:
            queryset = queryset.exclude(login_required=True)
        return queryset

    def get_search_queryset(self):
        # Infer the haystack index from the request language
        # and construct the results from it
        haystack_connection = get_haystack_connection_from_request(self.request)
        return SearchQuerySet(using=haystack_connection)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.get_query(self.form)
        context["form"] = self.form
        if self.object_list.query.backend.include_spelling:
            context["suggestion"] = self.form.get_suggestion()

        return context
