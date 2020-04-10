from data import models


def test_drivers_found_and_sorted():
    # This list needs to be updated whenever we add another driver
    expected_drivers = [('UsbipOverSSH', 'UsbipOverSSH'), ('USB_Quartermaster_VirtualHere', 'USB_Quartermaster_VirtualHere')]
    discovered_drivers = models.loaded_device_drivers()
    assert expected_drivers == discovered_drivers

# TODO: Test validation works
