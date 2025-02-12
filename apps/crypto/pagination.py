from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from collections import OrderedDict
from rest_framework import status


class CPageNumberPagination(PageNumberPagination):

    page_size = 10
    page_query_param = "page"

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        page_count = response.data.get("count") // self.page_size
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", response.data.get("next")),
                    ("previous", response.data.get("previous")),
                    ("page_count", page_count),
                    ("status", True),
                    ("status_code", status.HTTP_200_OK),
                    ("message", "Success"),
                    ("data", data),
                ]
            )
        )
