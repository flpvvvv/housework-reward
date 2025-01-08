import React, { useState, useEffect } from 'react';
import api from '../api';

const RecordForm = ({ form, setForm, onSubmit, submitLabel, currentImage, isLoading }) => {
  const [contributors, setContributors] = useState([]);
  const [isNewContributor, setIsNewContributor] = useState(false);

  useEffect(() => {
    api.get('/contributors/')
      .then(response => setContributors(response.data.results))
      .catch(err => console.error('Error fetching contributors:', err));
  }, []);

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <input
        type="datetime-local"
        value={form.time}
        onChange={(e) => setForm({ ...form, time: e.target.value })}
        className="border rounded p-2 w-full"
      />
      
      <div className="space-y-2">
        <div className="flex justify-end">
          <button
            type="button"
            onClick={() => {
              setIsNewContributor(!isNewContributor);
              setForm({ ...form, contributor_name: '' });
            }}
            className="text-sm text-blue-500 hover:text-blue-700"
          >
            {isNewContributor ? 'Select Existing' : 'Add New Contributor'}
          </button>
        </div>
        
        {isNewContributor ? (
          <input
            type="text"
            placeholder="New Contributor Name"
            value={form.contributor_name}
            onChange={(e) => setForm({ ...form, contributor_name: e.target.value })}
            className="border rounded p-2 w-full"
          />
        ) : (
          <select
            value={form.contributor_name}
            onChange={(e) => setForm({ ...form, contributor_name: e.target.value })}
            className="border rounded p-2 w-full"
          >
            <option value="">Select Contributor</option>
            {contributors.map(contributor => (
              <option key={contributor.id} value={contributor.name}>
                {contributor.name}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <label className="text-sm text-gray-600">Points: {form.points}</label>
          <input
            type="range"
            min="1"
            max="5"
            value={form.points}
            onChange={(e) => setForm({ ...form, points: parseInt(e.target.value) })}
            className="w-full"
          />
        </div>
      </div>

      <textarea
        placeholder="Note"
        value={form.note}
        onChange={(e) => setForm({ ...form, note: e.target.value })}
        className="border rounded p-2 w-full"
      />
      {currentImage && (
        <div className="mb-2">
          <img src={currentImage} alt="Current" className="max-w-xs" />
          <p className="text-sm text-gray-500">Current image</p>
        </div>
      )}
      <input
        type="file"
        onChange={(e) => setForm({ ...form, image: e.target.files[0] })}
        className="border rounded p-2 w-full"
      />
      <button 
        type="submit" 
        className="bg-blue-500 text-white rounded p-2 w-full"
        disabled={isLoading}
      >
        {submitLabel}
      </button>
    </form>
  );
};

export default RecordForm;
