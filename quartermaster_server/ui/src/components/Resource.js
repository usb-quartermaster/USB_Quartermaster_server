import React, {Component} from 'react';
import Device from "./Device";
import ReservationInformation from "./ReservationInformation";
import Button from 'react-bootstrap/Button';

class Resource extends Component {
    constructor(props) {
        super(props);
        let { resource } = props
        this.state = { resource: resource }
    }

    reserve_resource(resource) {
        console.log(resource)
    }
    
    render() {
        let { resource } = this.state
        let devices = resource.device_set
        return (
            <div>
                <p>{resource.name}</p>
                {
                    resource.used_for ? <ReservationInformation resource={resource}/> : <Button onClick={(resource) => this.reserve_resource(resource)}>Reserve</Button>
                }
                
                {devices.map(device => <Device key={device.name} device={device}/>)}
            </div>
        );
    }
}

export default Resource;
