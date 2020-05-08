import json

import pytest

from data.models import Device, Resource, Pool, RemoteHost


@pytest.fixture()
def sample_remote_host():
    return RemoteHost.objects.create(address='example.com', communicator='MockCommunicator',
                                     config_json='{}')


@pytest.fixture()
def sample_pool():
    return Pool.objects.create(name='TEST_POOL_DEVICE_MANAGER')


@pytest.fixture()
def sample_shared_resource(sample_pool, admin_user):
    pool = sample_pool
    return Resource.objects.create(pool=pool, name=f"RESOURCE_1", user=admin_user)


@pytest.fixture()
def sample_unshared_resource(sample_pool, admin_user):
    pool = sample_pool
    return Resource.objects.create(pool=pool, name=f"RESOURCE_2", user=None)


@pytest.fixture()
def sample_shared_device(sample_shared_resource, sample_remote_host):
    return Device.objects.create(resource=sample_shared_resource, driver="MockDevice",
                                 host=sample_remote_host, config_json='{}',
                                 name=f"Device 1")


@pytest.fixture()
def sample_unshared_device(sample_unshared_resource, sample_remote_host):
    return Device.objects.create(resource=sample_unshared_resource, driver="MockDevice",
                                 host=sample_remote_host, config_json='{}',
                                 name=f"Device 2")
