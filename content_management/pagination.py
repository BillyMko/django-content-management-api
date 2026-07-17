from rest_framework.pagination import PageNumberPagination

class ContentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "pagesize"
    max_page_size = 10