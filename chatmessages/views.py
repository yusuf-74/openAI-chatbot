from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Response as ChatResponse
from .serializers import MessageSerializer, ResponseSerializer,ViewMessageSerializer
from rest_framework.permissions import IsAuthenticated
import openai


def chatbot_response(user_input):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response["choices"][0]["text"]
    
class MessageView(APIView):
    def get(self, request):
        messages = Message.objects.filter(user = request.user.id)
        serializer = ViewMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["user"] = request.user.pk
        messageSerializer = MessageSerializer(data=data)
        if messageSerializer.is_valid():
            message = messageSerializer.save()
            response = chatbot_response(messageSerializer.data["text"])
            data={"text": response , "message": message.id}
            responseSerializer = ResponseSerializer(data=data)
            if responseSerializer.is_valid():
                responseSerializer.save()
            else :
                return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            res = ViewMessageSerializer(message)
            return Response(res.data, status=status.HTTP_201_CREATED)
        
        return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatView(LoginRequiredMixin,APIView):
    login_url = 'login'
    def get(self, request):
        messages = Message.objects.filter(user = request.user.id)
        serializer = ViewMessageSerializer(messages, many=True)
        context = {"messages": serializer.data}
        return render(request, 'messages/chat-view.html', context)
    
    def post(self, request):
        data = request.POST.copy()
        print(data)
        data["user"] = request.user.pk
        messageSerializer = MessageSerializer(data=data)
        if messageSerializer.is_valid():
            message = messageSerializer.save()
            response = chatbot_response(messageSerializer.data["text"])
            data={"text": response , "message": message.id}
            responseSerializer = ResponseSerializer(data=data)
            if responseSerializer.is_valid():
                responseSerializer.save()
            else :
                return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            res = ViewMessageSerializer(message)
            return redirect('chat')
        
        return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)