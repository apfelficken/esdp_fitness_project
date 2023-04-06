from django.core.exceptions import BadRequest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.utils.http import urlencode
from django.urls import reverse, reverse_lazy
from django.db.models import Count, QuerySet
from webapp.models import Client
from webapp.forms import ClientForm, AddGroupClient, SearchForm
from webapp.filters import ClientFilter
from django.db.models import Q
from typing import Optional, Union


class ClientListView(ListView):
    model = Client
    template_name: str = 'clients/clients_list.html'
    context_object_name: str = 'clients'
    paginate_by: int = 10

    def get_search_form(self) -> SearchForm:
        return SearchForm(self.request.GET)

    def get_search_value(self) -> Optional[str]:
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get(self, request, *args, **kwargs) -> Union[redirect, ListView]:
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Client]:
        clients = super().get_queryset()
        queryset = clients.filter(is_active=True).annotate(visit_count=Count('trainings'))
        if self.search_value:
            queryset = queryset.filter(
                Q(telegram_name__icontains=self.search_value) | Q(phone__icontains=self.search_value))
        return ClientFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filter'] = ClientFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = self.form
        if self.request.GET.get('is_paid'):
            context['query'] = urlencode({'is_paid': self.request.GET.get('is_paid')})
        elif self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class: ClientForm = ClientForm
    template_name: str = 'clients/client_create.html'

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(DetailView):
    model = Client
    template_name: str = 'clients/client_detail.html'

    def get_queryset(self) -> QuerySet[Client]:
        clients = super().get_queryset()
        queryset = clients.filter(is_active=True).annotate(visit_count=Count('trainings'))
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        payments = client.payments.order_by('-paid_at')
        paginator = Paginator(payments, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_active = Client.objects.active_clients().filter(pk=client.pk)
        context['form'] = AddGroupClient() if is_active and client.group is None else None
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['payments'] = page_obj.object_list
        return context


class ClientUpdateView(UpdateView):
    template_name = 'clients/client_update.html'
    model = Client
    form_class = ClientForm

    def get_success_url(self) -> str:
        return reverse('webapp:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    template_name: str = 'clients/client_delete.html'
    model = Client
    context_object_name: str = 'client'
    success_url: str = reverse_lazy('webapp:index')

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=int(kwargs.get('pk')))
        client.is_active = False
        client.group = None
        client.save()
        return redirect(self.success_url)


class ClientRestoreView(DeleteView):
    template_name: str = 'clients/client_restore.html'
    model = Client
    context_object_name: str = 'client'
    success_url: str = reverse_lazy('webapp:deleted_list')

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=int(kwargs.get('pk')))
        client.is_active = True
        client.save()
        return redirect(self.success_url)


class ClientDeletedListView(ListView):
    model = Client
    template_name: str = 'clients/clients_deleted_list.html'
    context_object_name: str = 'clients'
    paginate_by: int = 10

    def get_search_form(self) -> SearchForm:
        return SearchForm(self.request.GET)

    def get_search_value(self) -> Optional[str]:
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get(self, request, *args, **kwargs) -> Union[redirect, ListView]:
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Client]:
        clients = super().get_queryset()
        queryset = clients.filter(is_active=False).annotate(visit_count=Count('trainings'))
        if self.search_value:
            queryset = queryset.filter(
                Q(telegram_name__icontains=self.search_value) | Q(phone__icontains=self.search_value))
        return ClientFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filter'] = ClientFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = self.form
        if self.request.GET.get('is_paid'):
            context['query'] = urlencode({'is_paid': self.request.GET.get('is_paid')})
        elif self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ClientGroupUpdateView(View):
    def post(self, request, *args, **kwargs) -> HttpResponse:
        client_pk: int = kwargs.get('pk')
        group_id: int = int(request.POST.get('group_id'))
        is_active: bool = Client.objects.active_clients().filter(pk=client_pk)
        client: Client = get_object_or_404(Client, pk=client_pk)
        if is_active and client.group is None:
            client.group_id = group_id
            client.save()
            return redirect(self.get_redirect_url(group_id))
        raise BadRequest('Клиент неактивен или уже состоит в группе')

    def get_redirect_url(self, group_pk: int) -> str:
        return reverse('webapp:group_detail', kwargs={'pk': group_pk})
