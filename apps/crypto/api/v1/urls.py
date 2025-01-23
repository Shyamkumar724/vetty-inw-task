from django.urls import path
from .views import CoinListAPI, CoinCategoriesView, CoinMarketView, HealthCheck

urlpatterns = [
    path("v1/health-check", HealthCheck.as_view(), name="health_check_v1"),
    path("v1/coin-list", CoinListAPI.as_view(), name="coin_list_v1"),
    path(
        "v1/coin-categories", CoinCategoriesView.as_view(), name="coins_categories_v1"
    ),
    path("v1/coin-market", CoinMarketView.as_view(), name="coin_market_v1"),
]
