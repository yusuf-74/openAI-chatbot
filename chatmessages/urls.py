from django.urls import path
from .views import MessageView, Test

urlpatterns = [
    path('', MessageView.as_view(), name='message'),
    path('test/', Test.as_view(), name='test'),
]
