from django.contrib import admin
from chat import models

# master models
admin.site.register(models.ChatWindow)
admin.site.register(models.Message)
