import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import RecordForm from '../components/RecordForm';

const AddRecord = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    time: new Date().toISOString().slice(0, 16),
    contributor_name: '',
    points: 3,
    note: '',
    image: null,
  });
  const [status, setStatus] = useState({ message: '', error: false });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus({ message: 'Submitting...', error: false });
    
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null) formData.append(key, value);
    });

    try {
      await api.post('/housework/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus({ message: 'Record added successfully!', error: false });
      setTimeout(() => navigate('/'), 1500);
    } catch (error) {
      setStatus({ 
        message: error.response?.data || 'Error submitting record', 
        error: true 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 relative">
      <button 
        onClick={() => navigate('/')} 
        className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded-full text-xl font-bold"
      >
        ✕
      </button>
      <h1 className="text-2xl font-bold mb-4">Add New Record</h1>
      {status.message && (
        <div className={`p-2 mb-4 rounded ${status.error ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {status.message}
        </div>
      )}
      <RecordForm
        form={form}
        setForm={setForm}
        onSubmit={handleSubmit}
        submitLabel="Submit"
        isLoading={isLoading}
      />
    </div>
  );
};

export default AddRecord;
