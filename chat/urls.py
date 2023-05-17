from django.urls import path, re_path
from .views import index, room
from chat import views_api


app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('users/', views_api.UserListView.as_view(), name='users_list'),
    path('window/', views_api.ChatWindowMessageListView.as_view(), name='window_message_list'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]
