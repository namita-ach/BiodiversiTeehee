import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [species, setSpecies] = useState([]);
  const [newSpecies, setNewSpecies] = useState({
    name: '',
    category: '',
    location: '',
    date_observed: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/api/species')
      .then(response => setSpecies(response.data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);
  
  const addSpecies = () => {
    axios.post('http://localhost:5000/api/species', newSpecies)
      .then(response => {
        setSpecies([...species, newSpecies]);
        setNewSpecies({ name: '', category: '', location: '', date_observed: '' });
      })
      .catch(error => console.error('Error adding species:', error));
  };

  return (
    <div>
      <h1>Biodiversity Tracking</h1>
      <ul>
        {species.map((item, index) => (
          <li key={index}>{item.name} - {item.category}</li>
        ))}
      </ul>
      <input
        type="text"
        placeholder="Name"
        value={newSpecies.name}
        onChange={(e) => setNewSpecies({ ...newSpecies, name: e.target.value })}
      />
      <input
        type="text"
        placeholder="Category"
        value={newSpecies.category}
        onChange={(e) => setNewSpecies({ ...newSpecies, category: e.target.value })}
      />
      <input
        type="text"
        placeholder="Location"
        value={newSpecies.location}
        onChange={(e) => setNewSpecies({ ...newSpecies, location: e.target.value })}
      />
      <input
        type="date"
        value={newSpecies.date_observed}
        onChange={(e) => setNewSpecies({ ...newSpecies, date_observed: e.target.value })}
      />
      <button onClick={addSpecies}>Add Species</button>
    </div>
  );
}

export default App;
