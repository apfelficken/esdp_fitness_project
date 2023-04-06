from rest_framework.views import APIView
from django.http import JsonResponse
from constance import config
import json
from rest_framework import status


class AdminView(APIView):
    def get(self, *args: tuple, **kwargs: dict):
        cached_data = config.ADMIN
        if not cached_data:
            return JsonResponse({'error': 'No cached data found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            cached_data = json.dumps(int(cached_data))
            cached_data = json.loads(cached_data)
            return JsonResponse(cached_data, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
