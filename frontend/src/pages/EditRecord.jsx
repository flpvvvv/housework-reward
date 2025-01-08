import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api, { minioEndpoint } from '../api';
import RecordForm from '../components/RecordForm';

const getImageUrl = (imagePath) => {
  if (!imagePath) return null;
  return `${minioEndpoint}/${imagePath}`;
};

const EditRecord = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
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
        const response = await api.get(`/housework/${id}/`);
        const record = response.data;
        const formattedTime = new Date(record.record_time).toISOString().slice(0, 16);
        setForm({
          time: formattedTime,
          contributor_name: record.contributor.name,
          points: record.points,
          note: record.note,
          image: record.image,
        });
      } catch (error) {
        console.error('Error loading record:', error);
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
    setIsSubmitting(true);
    setStatus({ message: 'Updating...', error: false });
    
    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && (key !== 'image' || value instanceof File)) {
        formData.append(key, value);
      }
    });

    try {
      await api.put(`/housework/${id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus({ message: 'Record updated successfully!', error: false });
      setTimeout(() => navigate('/'), 1500);
    } catch (error) {
      setStatus({
        message: error.response?.data || 'Error updating record',
        error: true,
      });
    } finally {
      setIsSubmitting(false);
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
      <RecordForm
        form={form}
        setForm={setForm}
        onSubmit={handleSubmit}
        submitLabel="Update"
        currentImage={typeof form.image === 'string' ? getImageUrl(form.image) : null}
        isLoading={isSubmitting}
      />
      <button
        type="button"
        onClick={() => navigate('/')}
        className="mt-4 bg-gray-500 text-white rounded p-2 w-full"
      >
        Cancel
      </button>
    </div>
  );
};

export default EditRecord;
