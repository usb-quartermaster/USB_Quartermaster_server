import React from 'react';
import axios from 'axios';
import Pool from "./Pool";

const api_base = 'http://localhost:8000/api/v1'


class Pools extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pools: [],
            initialized: false,
            check_in_progress : false
        };

    }

    get_pools() {
        axios.get(`${api_base}/pool`)
            .then((response) => {
                    console.log(response)
                    this.setState({ pools: response.data, initialized: true })
                }
            )
            .catch((error) => {
                console.log(error)
                alert(`Unexpected response from server, rc=${error.status} message=${error.data}`)
            })
    }

    componentDidMount() {
        setInterval(() => this.get_pools(), 10000)
        this.get_pools()
    }

render()
{
    let { pools, initialized } = this.state
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
