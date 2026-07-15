from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Content, Category, ContentView
from .serializers import (RegisterSerializer,
                          ContentListSerializer,
                          ContentDetailSerializer,
                          ContentCreateSerializer,
                          CategorySerializer,
                          TagSerializer
                          )

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ContentListView(generics.ListAPIView):
    queryset = Content.objects.filter(is_published=True)
    serializer_class = ContentListSerializer


class ContentRetrieveView(generics.RetrieveAPIView):
    queryset = Content.objects.filter(is_published=True)
    serializer_class = ContentDetailSerializer
    lookup_field = "slug"

class ContentListCreateView(generics.ListCreateAPIView):
    queryset = Content.objects.all()

    def get_serializer_class(self):

        if self.request.method == "POST":
            return ContentCreateSerializer
        
        return ContentListSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)