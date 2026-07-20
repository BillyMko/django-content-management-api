from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Content, Category, ContentView
from .serializers import (RegisterSerializer,
                          ContentListSerializer,
                          ContentDetailSerializer,
                          ContentCreateSerializer,
                          CategorySerializer,
                          TagSerializer
                          )
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ContentPagination
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# class ContentListView(generics.ListAPIView):
#     queryset = Content.objects.filter(is_published=True)
#     serializer_class = ContentListSerializer


# class ContentRetrieveView(generics.RetrieveAPIView):
#     queryset = Content.objects.filter(is_published=True)
#     serializer_class = ContentDetailSerializer
#     lookup_field = "slug"

# class ContentListCreateView(generics.ListCreateAPIView):
#     queryset = Content.objects.all()

#     def get_serializer_class(self):

#         if self.request.method == "POST":
#             return ContentCreateSerializer
        
#         return ContentListSerializer
    
#     def get_permissions(self):
#         if self.request.method == "POST":
#             return [IsAuthenticated()]
        
#         return [AllowAny()]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


class ContentViewset(viewsets.ModelViewSet):

    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["difficulty", "category", "author"]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "title", "difficulty"]
    ordering = ["-created_at"]
    pagination_class = ContentPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Content.objects.filter(Q(is_published=True) | Q(author = self.request.user))
        
        return Content.objects.filter(is_published=True)

    def get_serializer_class(self):

        if self.action == "list":
            return ContentListSerializer
        
        if self.action == "create":
            return ContentCreateSerializer
        
        return ContentDetailSerializer
        
    def get_permissions(self):
        
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]    
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=["post"],
            permission_classes=[IsAuthenticated])
    
    def publish(self, request, slug=None):
        content = self.get_object()
        content.is_published = True
        content.save()

        return Response({"message":"Content pusblished successfully"}, 
                        status=status.HTTP_200_OK
                        )