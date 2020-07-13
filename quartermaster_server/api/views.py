# Create your views here.

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import serializers, generics, status, permissions, authentication
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import Resource, Device, RemoteHost, Pool
from quartermaster.allocator import make_reservation, release_reservation, refresh_reservation


class Login(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'is_authenticated': 'true'
        }
        return Response(content)


class ResourceAuthentication(authentication.BaseAuthentication):
    """
    This allows the use of resources passwords to authenticate.
    On the face this doesn't look great but those passwords will only be presented to authenticated
    users and are rotated when a reservation is complete.
    """

    def authenticate(self, request):
        resource_pk = request.parser_context['kwargs']['resource_pk']
        resource_password = request.parser_context['kwargs']['resource_password']
        resource = Resource.objects.get(pk=resource_pk)

        if resource.user is None:
            return None
        if resource.use_password != resource_password:
            return None

        return (resource.user, None)


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteHost
        fields = ['address', 'type', 'communicator']


class DeviceSerializer(serializers.ModelSerializer):
    host = HostSerializer()

    class Meta:
        model = Device
        fields = ['driver', 'name', 'host']


class ResourceSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField()
    device_set = DeviceSerializer(many=True)

    class Meta:
        model = Resource
        fields = ['user', 'used_for', 'last_reserved', 'last_check_in', 'name', 'device_set', 'resource_url']

    def get_resource_url(self, obj):
        return settings.SERVER_BASE_URL + reverse('api:show_resource', kwargs={"resource_pk": obj.name})


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = ['name']


class ResourceDetail(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_url_kwarg = 'resource_pk'


class PoolList(generics.ListAPIView, ListModelMixin):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer


class ResourceList(generics.ListAPIView, ListModelMixin):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class PoolResourceList(ResourceList):

    def get_queryset(self):
        pool_pk = self.kwargs['pool_pk']
        return self.queryset.filter(pool=pool_pk)


class ReservationSerializer(ResourceSerializer):
    reservation_url = serializers.SerializerMethodField()
    lookup_url_kwarg = 'resource_pk'

    class Meta:
        model = Resource
        fields = ResourceSerializer.Meta.fields + ['reservation_url', 'reservation_expiration']

    def get_reservation_url(self, resource_pk):
        return settings.SERVER_BASE_URL + reverse('api:show_reservation', kwargs={"resource_pk": self.instance.pk})


class ReservationView(generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ReservationSerializer
    lookup_url_kwarg = 'resource_pk'
    resource: Resource
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.resource: Resource = self.get_object()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.resource)
        if self.resource.user is None:
            make_reservation(self.resource, user=request.user, used_for=request.data.get('used_for', 'API User'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif self.resource.user == request.user:
            return Response(serializer.data)
        else:
            return JsonResponse({"message": f"The resource in use by another user, {self.resource.user.username}"},
                                status=403)

    def get(self, request, *args, **kwargs):
        if self.resource.user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif self.resource.user == request.user:
            serializer = self.get_serializer(self.resource)
            return Response(serializer.data)
        else:
            return JsonResponse({"message": f"The resource in use by another user, {self.resource.user.username}"},
                                status=403)

    def delete(self, request, *args, **kwargs):
        release_reservation(self.resource)
        self.resource.refresh_from_db()
        serializer = self.get_serializer(self.resource)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        refresh_reservation(resource=self.resource)
        self.resource.refresh_from_db()
        serializer = self.get_serializer(self.resource)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def head(self, request, *args, **kwargs):
        if self.resource.user == request.user:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ReservationDjangoAuthView(ReservationView):
    pass


class ReservationResourcePasswordView(ReservationView):
    authentication_classes = [ResourceAuthentication]
