import React, { useState } from 'react';

const AddRecord = () => {
  const [form, setForm] = useState({
    time: new Date().toISOString(),
    contributor: '',
    points: 3,
    note: '',
    image: null,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Record Submitted:', form);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Add New Record</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="datetime-local"
          value={form.time}
          onChange={(e) => setForm({ ...form, time: e.target.value })}
          className="border rounded p-2 w-full"
        />
        <input
          type="text"
          placeholder="Contributor"
          value={form.contributor}
          onChange={(e) => setForm({ ...form, contributor: e.target.value })}
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
