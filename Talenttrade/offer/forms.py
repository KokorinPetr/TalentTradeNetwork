from django import forms

from .models import Offer, UserProfile


class OfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = (
            'title', 'description', 'categories', 'price'
        )
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)
