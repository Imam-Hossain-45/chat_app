from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('api-token-auth/', views.obtain_jwt_token, name='login_token'),
]
