from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination



class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  
    max_limit = 100 
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.count,
            'limit': self.limit,
            'offset': self.offset,
            'results': data
        })