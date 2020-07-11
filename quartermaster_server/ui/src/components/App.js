import React from 'react';
import './App.css';
import Pools from "./Pools";
import Resources from "./Resources";

const api_base = 'http://localhost:8000/api/v1'


class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="App">
                <Pools></Pools>
                <Resources></Resources>
            </div>
        );
    }

}

//
// function App() {
//
//     return (
//         <div className="App">
//             <header className="App-header">
//                 Login is
//                 Learn React
//             </header>
//         </div>
//     );
// }

export default App;
