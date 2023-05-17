from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat import serializers, models
from accounts.serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Purpose: Users List except current user
    Url: /chat/users/
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            qs = User.objects.filter().exclude(id=request.user.id)
        except Exception as err:
            return Response({'details': str(err)}, status=status.HTTP_400_BAD_REQUEST)

        response_data = self.get_serializer(qs, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)


class ChatWindowMessageListView(generics.ListAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Purpose: Chat Window of current and requested user
    Url: /chat/window/
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChatWindowSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'user' not in data or not data['user'] or not User.objects.filter(id=data['user']).exists():
            return Response({'details': 'valid user needed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_user = User.objects.get(id=data['user'])
        except Exception as err:
            return Response({'details': str(err)}, status=status.HTTP_400_BAD_REQUEST)

        if chat_user == request.user:
            return Response({'details': 'valid user needed for chat'}, status=status.HTTP_400_BAD_REQUEST)
        
        window_qs = models.ChatWindow.objects.filter(
            Q(user1=request.user, user2=chat_user) |
            Q(user2=request.user, user1=chat_user)
        )

        if window_qs.exists():
            obj = window_qs[0]
        else:
            try:
                obj = models.ChatWindow.objects.create(user1=request.user, user2=chat_user)
            except:
                window_qs = models.ChatWindow.objects.filter(
                    Q(user1=request.user, user2=chat_user) |
                    Q(user2=request.user, user1=chat_user)
                )

                if window_qs.exists():
                    obj = window_qs[0]
                else:
                    obj = None

        response_data = self.get_serializer(obj).data
        return Response(response_data, status=status.HTTP_200_OK)
