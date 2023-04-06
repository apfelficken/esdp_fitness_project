from django.shortcuts import get_object_or_404
from rest_framework import serializers
from webapp.models import Client, Group, Training


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['telegram_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class TrainingSerializer(serializers.ModelSerializer):
    telegram_name: str = serializers.CharField()

    class Meta:
        model = Training
        fields = ['telegram_name']

    def save(self, **kwargs) -> Training:
        telegram_name: str = self.validated_data['telegram_name']
        client = get_object_or_404(Client, telegram_name=telegram_name)
        group = client.group
        training = Training.objects.create(client=client, group=group)
        training.save()
        return training
