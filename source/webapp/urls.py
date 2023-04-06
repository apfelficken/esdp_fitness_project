from django.urls import path, include
from webapp.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    ClientGroupUpdateView, ClientDeletedListView, ClientRestoreView,\
    PaymentCreateView,  PaymentUpdateView, PaymentDeleteView, \
    CoachListView, CoachDetailView, CoachCreateView, CoachUpdateView, CoachDeleteView, CoachStatisticsView,\
    GroupListView, GroupDetailView, GroupCreateView, GroupUpdateView, GroupDeleteView, \
    GroupClientUpdateView, GroupClientDeleteView, \
    TrainingListView, TrainingCreateView, TrainingDeleteView, \
    SendInvite, Mailing, GroupMailing


app_name = 'webapp'

client_url = [
    path('', ClientListView.as_view(), name='index'),
    path('deleted/list', ClientDeletedListView.as_view(), name='deleted_list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('<int:pk>/client/restore', ClientRestoreView.as_view(), name='client_restore'),
    path('<int:pk>/client/update', ClientGroupUpdateView.as_view(), name='client_group_update'),
]

payment_url = [
    path('<int:pk>/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('<int:pk>/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
]

coach_url = [
    path('list/', CoachListView.as_view(), name='coach_list'),
    path('<int:pk>/detail/', CoachDetailView.as_view(), name='coach_detail'),
    path('create/', CoachCreateView.as_view(), name='coach_create'),
    path('<int:pk>/update/', CoachUpdateView.as_view(), name='coach_update'),
    path('<int:pk>/delete/', CoachDeleteView.as_view(), name='coach_delete'),
    path('statistics/', CoachStatisticsView.as_view(), name='coach_statistics'),

]

group_url = [
    path('list/', GroupListView.as_view(), name='group_list'),
    path('<int:pk>/detail/', GroupDetailView.as_view(), name='group_detail'),
    path('create/', GroupCreateView.as_view(), name='group_create'),
    path('<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),
    path('<int:pk>/client/update', GroupClientUpdateView.as_view(), name='group_client_update'),
    path('<int:pk>/client/delete', GroupClientDeleteView.as_view(), name='group_client_delete'),
]


training_url = [
    path('<int:pk>/list/', TrainingListView.as_view(), name='training_list'),
    path('<int:pk>/create/', TrainingCreateView.as_view(), name='training_create'),
    path('<int:pk>/delete/', TrainingDeleteView.as_view(), name='training_delete'),
]

send_invitee_massage_url = [
    path('<int:pk>/invite/', SendInvite.as_view(), name='send_invite'),
    path('<int:pk>/group/', GroupMailing.as_view(), name='send_group_mailing'),
    path('mailing/', Mailing.as_view(), name='mailing_page'),
]

urlpatterns = [
    path('', include(client_url)),
    path('client/', include(client_url)),
    path('payment/', include(payment_url)),
    path('coach/', include(coach_url)),
    path('group/', include(group_url)),
    path('training/', include(training_url)),
    path('send/', include(send_invitee_massage_url))
]