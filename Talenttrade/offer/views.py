from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from .models import Offer, FAQ, Category, User, Review

def index(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category_filter')

    offers = Offer.objects.all()

    if selected_category:
        offers = offers.filter(categories__name=selected_category)
    context = {
        'offers': offers,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'offers/index.html', context)


def offer_detail(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    reviews = Review.objects.filter(offer=offer)
    mean_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    context = {
        'offer': offer,
        'reviews': reviews,
        'mean_rating': mean_rating
    }
    return render(request, 'offers/offer_detail.html', context)


def search_view(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = Offer.objects.filter(title__icontains=query)
    context = {
        'results': results,
        'query': query
    }
    return render(request, 'offers/search_offer.html', context)


def faq_view(request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs
    }
    return render(request, 'offers/faq.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    offers = user.offers.all()
    context = {
        'user': user,
        'offers': offers
    }
    return render(request, 'offers/profile.html', context)
