from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class DefaultPagination(PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
