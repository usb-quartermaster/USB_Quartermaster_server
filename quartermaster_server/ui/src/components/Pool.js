import React from 'react';


function Pool(props) {
    let { pool } = props
    return (
        <p>{pool.name}</p>
    )
}

export default Pool;
