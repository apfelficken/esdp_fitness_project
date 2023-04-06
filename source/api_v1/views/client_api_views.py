from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from api_v1.serializers import ClientSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Client, Coach, Group
from rest_framework import status


class ClientListAPIView(ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.query_params.get('active') == 'true':
            return Client.objects.active_clients()
        else:
            return Client.objects.all()


class ClientDetailAPIView(RetrieveAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.active_clients()


class ClientCreateAPIView(CreateAPIView):
    serializer_class = ClientSerializer


class CheckAPIView(APIView):
    def get(self, request: HttpRequest, telegram_name: str, *args: tuple, **kwargs: dict) -> Response:
        try:
            Client.objects.get(telegram_name=telegram_name)
            return Response({'result': 'client'}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            try:
                Coach.objects.get(telegram_name=telegram_name)
                return Response({'result': 'coach'}, status=status.HTTP_200_OK)
            except Coach.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class ActiveClientsInGroupAPIView(ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self) -> QuerySet:
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        if self.request.query_params.get('active') == 'true':
            return Client.objects.active_clients().filter(group=group)
        else:
            return Client.objects.all().filter(group=group)