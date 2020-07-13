import React, {Component} from 'react';
import Button from "react-bootstrap/Button";
import {qm_server} from "./Config";
import Devices from "./Devices";

class ReserveredResource extends Component {
    constructor(props) {
        super(props);
        let {resource, update_func} = props
        this.update_resource = update_func
        this.state = {resource: resource}
    }

    release_reservation = () => {
        let resource = this.state.resource
        let path = `resource/${resource.name}/reservation`
        qm_server.delete(path).then((resp) => this.update_resource(resp.data))
    }

    render() {
        let resource = this.state.resource

        return (
            <div>
                <p>{resource.name} Used by {resource.used_for}</p>
                <Button onClick={(e) => this.release_reservation(e, resource)}>Release</Button>
                <Devices devices={resource.device_set}></Devices>
            </div>
        );
    }
}


export default ReserveredResource;
