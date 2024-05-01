from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from djmoney.models.fields import MoneyField
from djmoney.money import Money

User = get_user_model()

TEXT_LIMIT = 15


class Offer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    price = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=Money(10, 'USD')
    )
    categories = models.ManyToManyField(
        'Category',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        default_related_name = 'offers'

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:TEXT_LIMIT]


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.question[:TEXT_LIMIT]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
