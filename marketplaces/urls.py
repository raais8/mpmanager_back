from django.urls import path

from . import views

app_name = 'marketplaces'
urlpatterns = [
    path('api/marketplaces/', views.MarketplaceListView.as_view(), name='marketplaces'),
]