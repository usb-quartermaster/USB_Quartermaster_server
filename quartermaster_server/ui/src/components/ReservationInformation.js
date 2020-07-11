import React from 'react';

function ReservationInformation(props) {
    let { resource } = props
    return (
        <div>{resource.used_for}</div>
    );
}

export default ReservationInformation;
