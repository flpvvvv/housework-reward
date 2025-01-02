import React, { useEffect, useState } from 'react';

const ViewRecords = () => {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetch('/api/records/')
      .then((res) => res.json())
      .then((data) => setRecords(data));
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Records</h1>
      <ul className="space-y-4">
        {records.map((record) => (
          <li key={record.id} className="border rounded p-4">
            <p><strong>Time:</strong> {record.time}</p>
            <p><strong>Contributor:</strong> {record.contributor}</p>
            <p><strong>Points:</strong> {record.points}</p>
            <p><strong>Note:</strong> {record.note}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ViewRecords;
