import React, { useState } from 'react';
import api from '../api';

const AddRecord = () => {
  const [form, setForm] = useState({
    time: new Date().toISOString(),
    contributor_name: '',  // changed from contributor
    points: 3,
    note: '',
    image: null,
  });
  const [status, setStatus] = useState({ message: '', error: false });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ message: 'Submitting...', error: false });
    
    const formData = new FormData();
    formData.append('time', form.time);
    formData.append('contributor_name', form.contributor_name);  // changed from contributor
    formData.append('points', form.points);
    formData.append('note', form.note);
    if (form.image) {
      formData.append('image', form.image);
    }

    try {
      await api.post('/records/add/', formData, {  // changed endpoint
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setStatus({ message: 'Record added successfully!', error: false });
      // Reset form
      setForm({
        time: new Date().toISOString(),
        contributor_name: '',
        points: 3,
        note: '',
        image: null,
      });
    } catch (error) {
      setStatus({ 
        message: error.response?.data || 'Error submitting record', 
        error: true 
      });
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Add New Record</h1>
      {status.message && (
        <div className={`p-2 mb-4 rounded ${status.error ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {status.message}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="datetime-local"
          value={form.time}
          onChange={(e) => setForm({ ...form, time: e.target.value })}
          className="border rounded p-2 w-full"
        />
        <input
          type="text"
          placeholder="Contributor Name"
          value={form.contributor_name}
          onChange={(e) => setForm({ ...form, contributor_name: e.target.value })}
          className="border rounded p-2 w-full"
        />
        <input
          type="number"
          min="1"
          max="5"
          value={form.points}
          onChange={(e) => setForm({ ...form, points: parseInt(e.target.value) })}
          className="border rounded p-2 w-full"
        />
        <textarea
          placeholder="Note"
          value={form.note}
          onChange={(e) => setForm({ ...form, note: e.target.value })}
          className="border rounded p-2 w-full"
        />
        <input
          type="file"
          onChange={(e) => setForm({ ...form, image: e.target.files[0] })}
          className="border rounded p-2 w-full"
        />
        <button type="submit" className="bg-blue-500 text-white rounded p-2 w-full">
          Submit
        </button>
      </form>
    </div>
  );
};

export default AddRecord;
