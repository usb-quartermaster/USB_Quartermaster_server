
* Create agent to run on remote servers to manage local devices that are being shared.
    This would have all the intelligence on how to accommodate OS differences
    This would install kernel modules as needed
    Will have to figure out plugin support for different server or just bake them in.
 
 When remote commands fail raise good errors in GUI
    
Update jobs to have pre and post scripts for sharing and unsharing
  Agent side or server side
  Add toggle to enable/disable script execution

Add client api for retrieving reservation record

Resources for USB power switching
  https://acroname.com/store/s79-usbhub-3p
  https://www.crowdsupply.com/capable-robot-components/programmable-usb-hub/updates/production-update-part-ii
  https://www.yepkit.com/product/300115/YKUSHXS
  https://electronics.stackexchange.com/questions/393468/efficient-way-to-selectively-unpower-usb-ports
  https://www.smartspate.com/how-to-convert-a-basic-usb-hub-into-driven-one/

   
Tasks to update device status are not scalable as they are done serially. Look ay making them async, or break them up into subtasks.
    Move host information to separate table
    Set up tasks to process hosts in parallel
    Merge checks for share state and online state so only one connection is needed for both

Windows support

Update client to have a wait for connections command
   background mode?
     decide where to log

Andriod ADB support
    VirtualHere driver works better
        I think there is a issue with the USBIP driver where adb size limits on reads are not honored.



Create autocomplete for adding host
    automatically retrieve host key
    display host key in record as read only

Create autocomplete for adding device
    automatically retrieve all suitable devices on host not being used elsewhere 
    add server arg to override default

Get rid of json_config. Move to simple key-value, maybe something else.


Remove dependence on usbip command, probe /sys directly
    """
    From usbip source code,
    /* Take only USB devices that are not hubs and do not have
     * the bInterfaceNumber attribute, i.e. are not interfaces.
     */
    """
    for i in $(find /sys/bus/usb/devices/); do [ ! -f $i/bInterfaceNumber ] && [ -f  "$i/bDeviceClass" ] && grep -qv '09' "$i/bDeviceClass" && echo $(basename $i),$(cat $i/idProduct),$(cat $i/idVendor),$(cat $i/manufacturer),$(cat $i/product); done

Remove remote discovery of VirtualHere client
    https://mathematica.stackexchange.com/questions/198187/how-to-read-a-named-pipe-on-windows
    Use echo and cat on posix
    
Update UI to group devices by pool


Make example driver app


Move drivers to plugin model
    Namespace usb_quartermaster_*
    Make USB_Quartermaster_common package with
        doc
    Figure out how to impliment integration plug-ins

Figure out how to handle plugins without hard coding them into deployment image
