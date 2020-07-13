import React from 'react';
import './App.css';
import Pools from "./Pools";
import Resources from "./Resources";


class App extends React.Component {

    render() {
        return (
            <div className="App">
                <Pools></Pools>
                <Resources></Resources>
            </div>
        );
    }

}

export default App;
