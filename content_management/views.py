from django.shortcuts import render
from rest_framework import generics
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