from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TotalCountHeaderPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "x-total-count": self.page.paginator.num_pages,
            "result": data
        })
