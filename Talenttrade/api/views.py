from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import SAFE_METHODS

from .serializers import (
    OfferReadSerializer, OfferEditSerializer,
    UserListSerializer, CategoriesSerializer,
    ReviewSerializer
)
from offer.models import Offer, User, Category, Review


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OfferReadSerializer
        return OfferEditSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return UserListSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
