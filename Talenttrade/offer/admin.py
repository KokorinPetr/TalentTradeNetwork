from django.contrib import admin
from .models import (Offer, Review, Category, FAQ)

admin.site.register(Offer)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(FAQ)
