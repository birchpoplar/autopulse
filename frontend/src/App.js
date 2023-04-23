import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { useState } from 'react';


function App() {
  const [cars, setCars] = useState([]);

  async function listCars() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/list_cars');
      setCars(response.data.cars);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={listCars}>List Cars</button>
        {/* Render the list of cars here */}
      </header>
    </div>
  );
}


export default App;
