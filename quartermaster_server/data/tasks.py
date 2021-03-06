import logging

from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import lock_task, db_periodic_task, db_task

from USB_Quartermaster_common import plugins
from data.models import Resource, RemoteHost
from quartermaster.allocator import release_reservation

logger = logging.getLogger(__name__)


@db_periodic_task(crontab(minute='*'))
@lock_task('update_reservations')
def update_reservations():
    """
    This cleaned up reservations whoes time has expired
    :return: None
    """

    for resource in Resource.objects.filter(user=None):
        if now() > resource.reservation_expiration or now() > resource.checkin_expiration:
            release_reservation(resource)


@db_periodic_task(crontab(minute='*'))
@lock_task('update_host_state')
def confirm_device_state():
    """
    This task is responsible for scheduling tasks that update the
    Quartermaster system to reflect the real state of hardware on remote hosts

    :return: None
    """
    for host in RemoteHost.objects.all():
        update_host_devices(host)


@db_task()
def update_host_devices(host: RemoteHost):
    """
    This take examines every Quartermaster device configured in on a host to confirm if it is online or offline and 
    reachable.

    :param host: RemoteHost
    :return: None
    """

    # For each driver
    for host_driver_class in plugins.remote_host_classes():
        # If compatible with communicator
        if host.communicator not in host_driver_class.SUPPORTED_COMMUNICATORS \
                or host.type not in host_driver_class.SUPPORTED_HOST_TYPES:
            continue

        host_driver = host_driver_class(host=host)

        devices_to_update = host.device_set.filter(driver=host_driver_class.DEVICE_CLASS.__name__)

        if not host_driver.is_reachable:
            logger.exception(f"Could not reach host {host}")
            for device in devices_to_update:
                device.online = False
                device.save()
            continue

        # If no devices are being check do try to communicate with host as that could end up raising exceptions
        if devices_to_update.count() > 0:
            host_driver.update_device_states(devices_to_update)
