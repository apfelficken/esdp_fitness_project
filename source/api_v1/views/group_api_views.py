from rest_framework.generics import ListAPIView
from api_v1.serializers import GroupSerializer
from webapp.models import Group


class GroupListAPIView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(is_active=True)
