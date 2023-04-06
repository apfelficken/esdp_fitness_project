from datetime import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from webapp.models import Group
from api_v1.serializers import GroupSerializer


class GroupListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('api_v1:group_list')
        Group.objects.create(name='Group1', start_at=datetime.now().time())
        Group.objects.create(name='Group2', start_at=datetime.now().time(), is_active=False)

    def test_group_list(self):
        response = self.client.get(self.url)
        groups = Group.objects.filter(is_active=True)
        serializer = GroupSerializer(groups, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
