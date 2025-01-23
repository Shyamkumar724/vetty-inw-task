from rest_framework.views import Response, APIView
from apps.crypto.coingeko_api import CRYPTOAPI
from apps.crypto.pagination import CPageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from apps.crypto.helpers.health_check import check_third_party_service
from django.http import JsonResponse
from django.conf import settings


@extend_schema(
    summary="Health Check Endpoint",
    description="Returns the health status of the application and its third-party \n"
    "dependencies.",
    responses={
        200: OpenApiResponse(
            description="The application and all services are healthy.",
            examples={
                "application/json": {
                    "app_name": "Crypto Market",
                    "version": "1.0.0",
                    "status": "healthy",
                    "timestamp": "2025-01-21T12:00:00Z",
                    "services": {"crypto_api": {"status": "healthy"}},
                }
            },
        ),
        503: OpenApiResponse(
            description="The application or one of the services is unhealthy.",
            examples={
                "application/json": {
                    "app_name": "Crypto Market",
                    "version": "1.0.0",
                    "status": "unhealthy",
                    "timestamp": "2025-01-21T12:00:00Z",
                    "services": {
                        "crypto_api": {
                            "status": "unhealthy",
                            "error": "Request timeout.",
                        }
                    },
                }
            },
        ),
    },
    tags=["Health Check API"],
)
class HealthCheck(APIView):

    authentication_classes = [BasicAuthentication, TokenAuthentication]

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        app_info = {
            "app_name": "Crypto Market",
            "version": "1.0.0",
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        }

        third_party_services = {
            "crypto_api": f"{settings.CRYPTO_GECO_BASE_URL}/ping",
        }

        services_status = {}
        for service_name, service_url in third_party_services.items():
            services_status.update(check_third_party_service(service_name, service_url))

        # Update the app status if any service is unhealthy
        if any(
            service["status"] == "unhealthy" for service in services_status.values()
        ):
            app_info["status"] = "unhealthy"

        app_info["services"] = services_status
        return JsonResponse(app_info)


@extend_schema(
    summary="Retrieve a List of all the Coins",
    description="""
    This endpoint allows authenticated users to retrieve a paginated list of
    all available coins in the system. Each coin in the response includes relevant
    details such as its unique identifier and metadata.

    **Features:**
    - **Pagination:** Supports pagination with customizable page sizes using
      the `per_page` query parameter (default is 10 coins per page).
    - **Error Handling:** Provides a user-friendly error message in case of
      unexpected issues during the retrieval process.

    **Access Control:**
    - Accessible only by admin users or those granted specific permissions
      to view the list of coins.

    **Query Parameters:**
    - `per_page` (optional): Number of coins to include per page. Defaults to 10 if not
    specified.

    **Example Response:**
    ```json
    {
        "count": 100,
        "next": "http://api.example.com/coins/?page=2",
        "previous": null,
        "results": [
            {
                "id": "1",
                "name": "Bitcoin",
                "symbol": "BTC",
                "market_cap": "500000000000"
            },
            ...
        ]
    }
    ```
    """,
    tags=["Coins API"],
)
class CoinListAPI(APIView):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        try:
            coins = CRYPTOAPI.get_coins()
            paginator = CPageNumberPagination()
            paginator.page_size = request.query_params.get("per_page", 10)
            result_page = paginator.paginate_queryset(coins, request)
            return paginator.get_paginated_response(result_page)
        except Exception as e:
            return Response({"error": str(e)})


@extend_schema(
    summary="Retrieve a List of Coin Categories",
    description="""
    This endpoint allows authenticated users to retrieve a paginated list of
    all available coin categories in the system. Each category represents a
    grouping of coins based on specific criteria (e.g., technology,
    market sector, etc.).

    **Features:**
    - **Pagination:** Supports pagination with customizable page sizes using the
      `per_page` query parameter (default is 10 categories per page).
    - **Error Handling:** Returns an error message for unexpected issues.

    **Access Control:**
    - Accessible only by users with proper authentication and permissions.

    **Query Parameters:**
    - `per_page` (optional): Number of categories to include per page. Defaults
    to 10 if not specified.

    **Example Response:**
    ```json
    {
        "count": 20,
        "next": "http://api.example.com/coin-categories/?page=2",
        "previous": null,
        "results": [
            {
                "id": "1",
                "name": "DeFi",
                "description": "Decentralized Finance coins",
                "number_of_coins": 250
            },
            ...
        ]
    }
    ```
    """,
    tags=["Coin Categories API"],
)
class CoinCategoriesView(APIView):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        try:
            coins = CRYPTOAPI.get_coinCategory()
            paginator = CPageNumberPagination()
            paginator.page_size = request.query_params.get("per_page", 10)
            result_page = paginator.paginate_queryset(coins, request)
            return paginator.get_paginated_response(result_page)
        except Exception as e:
            return Response({"error": str(e)})


@extend_schema(
    summary="Retrieve Coin Market Data",
    description="""
    This endpoint allows authenticated users to fetch a paginated list of market data
    for all available coins. Market data includes details such as current price,
    market cap, trading volume, and other relevant metrics.

    **Features:**
    - **Pagination:** Supports pagination with customizable page sizes using the
      `per_page` query parameter (default is 10 coins per page).
    - **Error Handling:** Provides structured error messages in case of failures.

    **Access Control:**
    - Accessible only by users with proper authentication and permissions.

    **Query Parameters:**
    - `per_page` (optional): Number of market data entries to include per page.
    Defaults to 10 if not specified.

    **Example Response:**
    ```json
    {
        "count": 100,
        "next": "http://api.example.com/coin-market/?page=2",
        "previous": null,
        "results": [
            {
                "id": "1",
                "name": "Bitcoin",
                "symbol": "BTC",
                "price": 45000.00,
                "market_cap": 850000000000,
                "volume_24h": 35000000000
            },
            ...
        ]
    }
    ```
    """,
    tags=["Coin Market API"],
)
class CoinMarketView(APIView):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        try:
            coins = CRYPTOAPI.fetch_market_data()
            paginator = CPageNumberPagination()
            paginator.page_size = request.query_params.get("per_page", 10)
            result_page = paginator.paginate_queryset(coins, request)
            return paginator.get_paginated_response(result_page)
        except Exception as e:
            return Response({"error": str(e)})
