import React, { useEffect, useState } from 'react';
import api from '../api';

const ViewRecords = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await api.get('/records/');
        setRecords(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch records');
        console.error('Error fetching records:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
  }, []);

  if (loading) return <div className="container mx-auto p-4">Loading...</div>;
  if (error) return <div className="container mx-auto p-4 text-red-500">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Records</h1>
      {records.length === 0 ? (
        <p>No records found</p>
      ) : (
        <ul className="space-y-4">
          {records.map((record) => (
            <li key={record.id} className="border rounded p-4">
              <p><strong>Time:</strong> {new Date(record.time).toLocaleString()}</p>
              <p><strong>Contributor:</strong> {record.contributor}</p>
              <p><strong>Points:</strong> {record.points}</p>
              <p><strong>Note:</strong> {record.note}</p>
              {record.image && (
                <img src={record.image} alt="Record" className="mt-2 max-w-xs" />
              )}
              <button
                onClick={() => navigate(`/records/edit/${record.id}`)}
                className="mt-2 bg-blue-500 text-white rounded px-4 py-2"
              >
                Edit
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ViewRecords;
