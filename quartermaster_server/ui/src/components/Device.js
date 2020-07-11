import React from 'react';

function Device(props) {
    let {device} = props
    return (
        <div>{device.name} {device.driver}</div>
    );
}

export default Device;
