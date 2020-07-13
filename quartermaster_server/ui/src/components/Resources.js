import React from 'react';
import {qm_server, refresh_frequency_ms} from './Config';
import Resource from "./Resource";
import ReserveredResource from "./ReserveredResource";

class Resources extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            resources: [],
            initialized: false,
        };

    }

    get_resources() {
        const path = '/resource/';
        qm_server.get(path)
            .then((response) => {
                    this.setState({resources: response.data, initialized: true})
                }
            )
            .catch((error) => {
                console.log(error)
                alert(`Unexpected response from server, path=${path}, rc=${error.status} message=${error.data}`)
            })
    }

    componentDidMount() {
        setInterval(() => this.get_resources(), refresh_frequency_ms)
        this.get_resources()
    }

    update_resource(updated_resource) {
        const update_resource = (original_resource) => {
            if (original_resource.name === updated_resource.name)
                return updated_resource
            else
                return original_resource
        }
        let new_state = {resources: this.state.resources.map(update_resource), ...this.state}
        console.log(new_state)
        this.setState(new_state)
    }

    render() {
        let {resources, initialized} = this.state
        if (resources.length) {
            return (
                <div>{resources.map(resource => {
                    return (resource.user ? <ReserveredResource key={resource.name} resource={resource}
                                                                update_func={this.update_resource.bind(this)}/> :
                        <Resource key={resource.name} resource={resource}
                                  update_func={this.update_resource.bind(this)}/>)
                })}</div>
            )
        } else if (initialized) {
            return (<p>No resources found</p>)
        } else {
            return (<p>Retrieving resources</p>)
        }
    }

}

export default Resources;
