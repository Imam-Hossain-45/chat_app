from rest_framework import serializers
from chat import models


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'MessageSerializer'
        model = models.Message
        fields = ('id', 'message', 'author')


class ChatWindowSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        ref_name = 'ChatWindowSerializer'
        model = models.ChatWindow
        fields = ('id', 'user1', 'user2', 'messages')

    def get_messages(self, obj):
        try:
            return MessageSerializer(models.Message.objects.filter(window=obj).order_by('id'), many=True).data
        except Exception as err:
            print(str(err))
            return []
