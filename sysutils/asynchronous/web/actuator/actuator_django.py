"""
Something likes https://www.baeldung.com/spring-boot-actuators
"""

from django.http import JsonResponse
from .actuator_runtime import get_info


def actuator(request):
    data = get_info(request)
    return JsonResponse(dict(data))
