import logging
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, filters

from .permissions import DefaultRoleBasedPermissions

_logger = logging.getLogger(__name__)


class DefaultBaseViewSet(viewsets.ModelViewSet):

    @property
    def actual_model(self):
        return self.serializer_class.Meta.model

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as ex:
            _logger.debug("Exception: {}".format(ex))
            _logger.warning("Cannot destroy object {}".format(self.actual_model))
        return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        if obj:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            _logger.warning("Cannot create object {}".format(self.actual_model))
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        return serializer.save()


def owner_filter(model, user):
    if hasattr(model, 'owner'):
        return model.objects.filter(owner=user)
    else:
        return None


@permission_classes([DefaultRoleBasedPermissions])
class DefaultPermittedBaseViewSet(DefaultBaseViewSet):
    """ Provides Permission checking """

    def list(self, request, *args, **kwargs):
        from account.permission_checker import get_quireyset
        user = request.user
        model = self.actual_model

        # _logger.debug("*** LIST - Permissions. Model: {} User: {};".format(model, user))

        queryset = get_quireyset(user, model, mode='read')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_object(self):
        from rest_framework.generics import get_object_or_404

        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        # self.check_object_permissions(self.request, obj)

        return obj
