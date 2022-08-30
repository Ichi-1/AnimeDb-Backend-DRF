from rest_framework import viewsets, permissions, mixins


class UserPermissionsViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    '''
    Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsAdminUser]}
    '''

    permission_cls = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'partial_update': [permissions.IsAuthenticated],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission() for permission in self.permission_cls[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
