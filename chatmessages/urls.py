from django.urls import path
from .views import MessageView, ChatView

urlpatterns = [
    path('api/', MessageView.as_view(), name='message'),
    path('', ChatView.as_view(), name='chat'),
]
