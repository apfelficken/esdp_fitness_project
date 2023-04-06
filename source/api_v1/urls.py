from django.urls import path, include
from api_v1.views import ClientDetailAPIView, ClientCreateAPIView, CheckAPIView, ClientListAPIView, \
    ActiveClientsInGroupAPIView, GroupListAPIView, TrainingCreateAPIView

from api_v1.views.cache_api_views import AdminView

app_name: str = 'api_v1'

client_urls = [
    path('', ClientListAPIView.as_view(), name='client_list'),
    path('<int:pk>/', ClientDetailAPIView.as_view(), name='client_detail'),
    path('create/', ClientCreateAPIView.as_view(), name='client_create'),
    path('check/<str:telegram_name>/', CheckAPIView.as_view(), name='client_check'),
    path('group/<int:group_id>/', ActiveClientsInGroupAPIView.as_view(), name='client_in_group')
]

group_urls = [
    path('', GroupListAPIView.as_view(), name='group_list'),
]

training_urls = [
    path('create/', TrainingCreateAPIView.as_view(), name='training_create'),
]

cache_urls = [
    path('cache/', AdminView.as_view(), name='cache'),
]

urlpatterns = [
    path('client/', include(client_urls)),
    path('group/', include(group_urls)),
    path('training/', include(training_urls)),
    path('admin/', include(cache_urls)),
]
