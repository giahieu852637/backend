from rest_framework.pagination import PageNumberPagination

class BasePaginator(PageNumberPagination):
    page_size = 5