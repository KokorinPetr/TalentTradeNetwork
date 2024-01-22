from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, UserViewSet, CategoryViewSet, ReviewViewSet

app_name = 'api'

router = DefaultRouter()
router.register('offers', OfferViewSet, basename='offers')
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
