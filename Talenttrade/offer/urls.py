from django.urls import path

from . import views

app_name = 'offers'

urlpatterns = [
    path('offer/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    path('offer/<int:offer_id>/edit/', views.offer_edit, name='offer_edit'),
    path('offer/create/', views.offer_create, name='offer_create'),
    path('faq/', views.faq_view, name='FAQ' ),
    path('search/', views.search_view, name='search'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('', views.index, name='index'),
    
]
