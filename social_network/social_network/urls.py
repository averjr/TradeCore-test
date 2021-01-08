from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from publications.views import UserViewSet, PostViewSet
from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register('api/users', UserViewSet)
router.register('api/posts', PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
