import React from 'react';
import axios from 'axios';
import Resource from "./Resource";

const api_base = 'http://localhost:8000/api/v1'


class Resources extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            resources: [],
            initialized: false,
            check_in_progress: false
        };

    }

    get_resources() {
        axios.get(`${api_base}/resource`)
            .then((response) => {
                    console.log(response)
                    this.setState({ resources: response.data, initialized: true })
                }
            )
            .catch((error) => {
                console.log(error)
                alert(`Unexpected response from server, rc=${error.status} message=${error.data}`)
            })
    }

    componentDidMount() {
        setInterval(() => this.get_resources(), 10000)
        this.get_resources()
    }

    render() {
        let { resources, initialized } = this.state
        if (resources.length) {
            return (<div>{resources.map(resource => <Resource key={resource.name} resource={resource}/>)}</div>)
        } else if (initialized) {
            return (<p>No pools found</p>)
        } else {
            return (<p>Retrieving pools</p>)
        }
    }

}

export default Resources;
