from django.urls import path
from .views import RegisterView, ContentViewset
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register("content", ContentViewset, basename="content")
urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    # path('content/<slug:slug>/', ContentRetrieveView.as_view(), name="content-retrieve"),
    # path('content/', ContentListCreateView.as_view(), name= "content-list-create")
]

urlpatterns = urlpatterns + router.urls
