import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const ViewRecords = () => {
  const navigate = useNavigate();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await api.get('/records/');
        setRecords(response.data.results || []);
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
        <>
          {/* Mobile view (cards) */}
          <div className="md:hidden space-y-4">
            {records.map((record) => (
              <div key={record.id} className="bg-white rounded-lg shadow p-4 border">
                <div className="grid grid-cols-2 gap-2">
                  <div className="font-semibold">Time:</div>
                  <div>{new Date(record.record_time).toLocaleString()}</div>
                  
                  <div className="font-semibold">Contributor:</div>
                  <div>{record.contributor.name}</div>
                  
                  <div className="font-semibold">Points:</div>
                  <div>{record.points}</div>
                  
                  <div className="font-semibold">Note:</div>
                  <div>{record.note}</div>
                </div>
                {record.image && (
                  <img src={record.image} alt="Record" className="mt-2 w-full h-auto rounded" />
                )}
                <button
                  onClick={() => navigate(`/records/edit/${record.id}`)}
                  className="mt-3 w-full bg-blue-500 text-white rounded px-4 py-2"
                >
                  Edit
                </button>
              </div>
            ))}
          </div>

          {/* Desktop view (table) */}
          <div className="hidden md:block overflow-x-auto">
            <table className="min-w-full table-auto border-collapse">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border px-4 py-2">Time</th>
                  <th className="border px-4 py-2">Contributor</th>
                  <th className="border px-4 py-2">Points</th>
                  <th className="border px-4 py-2">Note</th>
                  <th className="border px-4 py-2">Image</th>
                  <th className="border px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record) => (
                  <tr key={record.id} className="border hover:bg-gray-50">
                    <td className="border px-4 py-2">{new Date(record.record_time).toLocaleString()}</td>
                    <td className="border px-4 py-2">{record.contributor.name}</td>
                    <td className="border px-4 py-2">{record.points}</td>
                    <td className="border px-4 py-2">{record.note}</td>
                    <td className="border px-4 py-2">
                      {record.image && (
                        <img src={record.image} alt="Record" className="h-20 w-auto" />
                      )}
                    </td>
                    <td className="border px-4 py-2">
                      <button
                        onClick={() => navigate(`/records/edit/${record.id}`)}
                        className="bg-blue-500 text-white rounded px-3 py-1 text-sm"
                      >
                        Edit
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default ViewRecords;
