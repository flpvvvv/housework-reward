import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddRecord from './pages/AddRecord';
import EditRecord from './pages/EditRecord';
import ViewRecords from './pages/ViewRecords';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ViewRecords />} />
        <Route path="/add" element={<AddRecord />} />
        <Route path="/edit/:id" element={<EditRecord />} />
      </Routes>
    </Router>
  );
};

export default App;
