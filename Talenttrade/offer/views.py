from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Offer, FAQ, Category, User, Review
from .forms import OfferForm


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
        'mean_rating': mean_rating,
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



@login_required
@csrf_exempt
def offer_create(request):
    form = OfferForm(
        request.POST or None
    )
    if not form.is_valid():
        return render(request, 'offers/offer_create.html', {'form': form})
    offer = form.save(commit=False)
    offer.user = request.user
    offer.save()
    offer.categories.clear()
    offer.categories.add(*form.cleaned_data['categories'])
    return redirect('offers:profile', request.user)


@login_required
@csrf_exempt
def offer_edit(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    form = OfferForm(
        request.POST or None,
        files=request.FILES or None,
        instance=offer
    )
    user = request.user
    context = {
        'offer': offer,
        'form': form,
        'is_edit': True
    }
    if user != offer.user:
        return redirect('offers:offer_detail', offer_id)
    if form.is_valid():
        form.save()
        return redirect('offers:offer_detail', offer_id)
    return render(request, 'offers/offer_create.html', context)
