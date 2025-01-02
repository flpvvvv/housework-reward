import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

const EditRecord = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState({ message: '', error: false });
  const [form, setForm] = useState({
    time: '',
    contributor_name: '',
    points: 3,
    note: '',
    image: null,
  });

  useEffect(() => {
    const fetchRecord = async () => {
      try {
        const response = await api.get(`/records/${id}/`);
        const record = response.data;
        setForm({
          time: record.time,
          contributor_name: record.contributor_name,
          points: record.points,
          note: record.note,
          image: record.image,
        });
      } catch (error) {
        setStatus({
          message: 'Failed to load record',
          error: true,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchRecord();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ message: 'Updating...', error: false });
    
    const formData = new FormData();
    formData.append('time', form.time);
    formData.append('contributor_name', form.contributor_name);
    formData.append('points', form.points);
    formData.append('note', form.note);
    if (form.image instanceof File) {
      formData.append('image', form.image);
    }

    try {
      await api.put(`/records/${id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setStatus({ message: 'Record updated successfully!', error: false });
      setTimeout(() => navigate('/records'), 1500);
    } catch (error) {
      setStatus({
        message: error.response?.data || 'Error updating record',
        error: true,
      });
    }
  };

  if (loading) return <div className="container mx-auto p-4">Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Edit Record</h1>
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
        {typeof form.image === 'string' && (
          <div className="mb-2">
            <img src={form.image} alt="Current" className="max-w-xs" />
            <p className="text-sm text-gray-500">Current image</p>
          </div>
        )}
        <input
          type="file"
          onChange={(e) => setForm({ ...form, image: e.target.files[0] })}
          className="border rounded p-2 w-full"
        />
        <div className="flex space-x-4">
          <button type="submit" className="bg-blue-500 text-white rounded p-2 flex-1">
            Update
          </button>
          <button
            type="button"
            onClick={() => navigate('/records')}
            className="bg-gray-500 text-white rounded p-2 flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditRecord;
