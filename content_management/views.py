from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Content, Category, ContentView, Tag
from .serializers import (RegisterSerializer,
                          ContentListSerializer,
                          ContentDetailSerializer,
                          ContentCreateSerializer,
                          CategorySerializer,
                          TagSerializer
                          )
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (SearchFilter, 
                                    OrderingFilter)
from .pagination import ContentPagination
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import (IsAdmin,
                          IsApprovedInstructor,
                          IsAuthorOrAdmin)
from .filters import ContentFilter

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    queryset = User.objects.all()

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])

    def approve(self, request, id = None):
        user = self.get_object()
        user.status = "approve"
        user.save()

        return Response({"message": "Instructor approved successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    
    def reject(self, request, id = None):
        user = self.get_object()
        if user.role != "instructor":
            return Response({"message": "Only an instructor can be rejected"}, status=status.HTTP_400_BAD_REQUEST)
        user.status = "rejected"
        user.save()

        return Response({"message": "Instructor application rejected successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])

    def suspend(self, request, id = None):
        user = self.get_object()
        if user.role != "instructor":
            return Response({"message": "Only an instructor can be rejected"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.status != "approved":
            return Response({"message": "Only approved instructors can be suspended"}, status=status.HTTP_400_BAD_REQUEST)
        user.status = "suspended"
        user.save()

        return Response({"message": "Instructor suspended successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])

    def reinstate(self, request, id = None):
        user = self.get_object()
        if user.role != "instructor":
            return Response({"message": "Only an instructor can be reinstated"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.status != "suspended":
            return Response({"message": "Only suspended instructors can be reinstated"}, status=status.HTTP_400_BAD_REQUEST)
        user.status = "approved"
        user.save()

        return Response({"message": "Instructor reinstated successfully"}, status=status.HTTP_200_OK)

class ContentViewset(viewsets.ModelViewSet):


    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = ContentFilter
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
        
        if self.action == "create":
            return [IsApprovedInstructor()]
        
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsApprovedInstructor(), IsAuthorOrAdmin()]
        
        if self.action =="stats":
            return [AllowAny()]
        
        return [IsAuthenticated()]    
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=["post"],
            permission_classes=[IsAuthorOrAdmin])
    
    def publish(self, request, slug=None):
        content = self.get_object()
        content.is_published = True
        content.status = "published"
        content.save()

        return Response(
                        {"message":"Content pusblished successfully"}, 
                        status=status.HTTP_200_OK
                        )
    
    @action(detail=True,
            methods=["post"],
            permission_classes=[IsAuthorOrAdmin])
    
    def archive(self, request, slug=None):
        content_obj = self.get_object()
        content.is_published = False
        content.status = "archived"
        content.save()

        return Response(
                        {"message":"Content archived successfully"}, 
                        status=status.HTTP_200_OK
                        )
    
    @action(detail=True,
            methods=["get"])

    def stats(self, request, slug=None):
        content = self.get_object()

        return Response({
            "content_id": content.id,
            "title": content.title,
            "total views": content.views.count()
        })

    def retrieve(self, request, *args, **kwargs):
        content_obj = self.get_object()
        if request.user.is_authenticated == True:
            user = request.user
        else:
            user = None
        
        ContentView.objects.create(user = user, content= content_obj)
        serializer_obj = ContentDetailSerializer(content_obj)
        
        return Response(serializer_obj.data)
    
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        
        return [IsAdmin]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug" 

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        
        return [IsAdmin]

