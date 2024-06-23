from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.inspectors import PaginatorInspector
from drf_yasg import openapi
from typing import OrderedDict


class LimitOffsetPaginatorInspectorClass(PaginatorInspector):
    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict(
                (
                    (
                        "next_page",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            x_nullable=True,
                        ),
                    ),
                    (
                        "previous_page",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_URI,
                            x_nullable=True,
                        ),
                    ),
                    ("total_items", openapi.Schema(type=openapi.TYPE_INTEGER)),
                    ("actual_page", openapi.Schema(type=openapi.TYPE_INTEGER)),
                    ("total_page", openapi.Schema(type=openapi.TYPE_INTEGER)),
                    ("results", response_schema),
                )
            ),
            required=["results"],
        )


class DefaultPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 1
    page_query_description = "Número da página para busca"
    page_size_query_description = "Número de resultados que retornam por página"

    def get_paginated_response(self, data, return_only_data=True):
        data = {
            "next_page": self.get_next_link(),
            "previous_page": self.get_previous_link(),
            "total_items": self.page.paginator.count,
            "actual_page": self.page.number,
            "total_page": self.page.paginator.num_pages,
            "results": data,
        }
        if return_only_data:
            return data

        return Response(
            data
        )
