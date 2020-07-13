import React, {Component} from 'react';
import Button from 'react-bootstrap/Button';
import {qm_server} from "./Config";
import Devices from "./Devices";

class Resource extends Component {
    constructor(props) {
        super(props);
        let {resource, update_func} = props
        this.update_resource = update_func
        this.state = {resource: resource}
    }

    reserve_resource = (event, resource) => {
        console.log(resource)
        let path = `resource/${resource.name}/reservation`
        qm_server.post(path).then((resp) => this.update_resource(resp.data))
    }

    render() {
        let {resource} = this.state
        return (
            <div>
                <p>{resource.name}</p>
                <Button onClick={(e) => this.reserve_resource(e, resource)}>Reserve</Button>
                <Devices devices={resource.device_set}></Devices>
            </div>
        );
    }
}

export default Resource;
