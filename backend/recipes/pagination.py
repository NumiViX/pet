from rest_framework.pagination import PageNumberPagination

from backend.variables import PAGE_SIZE_NUM


class NewPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE_NUM
