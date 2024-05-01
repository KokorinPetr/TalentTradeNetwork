from rest_framework import serializers

from djoser.serializers import (
    UserSerializer,
)
from django.db.models import Avg
from django.shortcuts import get_list_or_404, get_object_or_404

from offer.models import Offer, Category, User, Review


class UserListSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description',)


class ReviewSerializer(serializers.ModelSerializer):
    offer = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)
    user = UserListSerializer()

    class Meta:
        model = Review
        fields = ("id", "text", "rating", "created_at", "user", "offer")

    def get_offer(self, obj):
        return obj.offer.title


class OfferReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'created_at',)


class OfferReadSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True)
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)
    user = UserListSerializer(read_only=True)
    mean_rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = (
           "id", "categories", "created_at",
           "user", "title", "description",
           "mean_rating", "reviews"
        )

    def get_mean_rating(self, obj):
        reviews = Review.objects.filter(offer=obj)
        mean_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if mean_rating is not None:
            return mean_rating
        return 'No reviews yet'

    def get_reviews(self, obj):
        reviews = Review.objects.filter(offer=obj)
        return OfferReviewSerializer(reviews, many=True).data


class OfferEditSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %B %Y', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = ('__all__')

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        offer = Offer.objects.create(**validated_data)
        offer.categories.set(categories)
        return offer
