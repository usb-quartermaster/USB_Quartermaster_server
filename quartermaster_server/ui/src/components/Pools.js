import React from 'react';
import {qm_server, refresh_frequency_ms} from './Config';
import Pool from "./Pool";


class Pools extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pools: [],
            initialized: false,
            check_in_progress: false
        };

    }

    get_pools() {
        const path='/pool/'
        qm_server.get(path)
            .then((response) => {
                    this.setState({pools: response.data, initialized: true})
                }
            )
            .catch((error) => {
                console.log(error)
                alert(`Unexpected response from server, path=${path}, rc=${error.status} message=${error.data}`)
            })
    }

    componentDidMount() {
        setInterval(() => this.get_pools(), refresh_frequency_ms)
        this.get_pools()
    }

    render() {
        let {pools, initialized} = this.state
        if (pools.length) {
            return (<div>{pools.map(pool => <Pool key={pool.name} pool={pool}/>)}</div>)
        } else if (initialized) {
            return (<p>No pools found</p>)
        } else {
            return (<p>Retrieving pools</p>)
        }
    }

}

export default Pools;
