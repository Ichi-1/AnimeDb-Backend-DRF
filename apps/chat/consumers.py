from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import CreateModelMixin


class LiveConsumer(CreateModelMixin, GenericAsyncAPIConsumer):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
