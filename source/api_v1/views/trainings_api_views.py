from rest_framework.generics import CreateAPIView
from api_v1.serializers import TrainingSerializer


class TrainingCreateAPIView(CreateAPIView):
    serializer_class = TrainingSerializer
