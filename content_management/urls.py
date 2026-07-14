from django.urls import path
from .views import RegisterView, ContentListView, ContentRetrieveView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('content/', ContentListView.as_view()),
    path('content/<slug:slug>/', ContentRetrieveView.as_view())
]
