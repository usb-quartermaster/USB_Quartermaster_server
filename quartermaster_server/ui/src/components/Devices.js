import React from 'react';

function Devices(props) {
    let {devices} = props
    return (
        <div>{devices.map(device => <div key={device.name}>{device.name} {device.driver}</div>)}</div>
    );
}

export default Devices;
