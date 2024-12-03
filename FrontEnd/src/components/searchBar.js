import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); // For error handling
  const navigate = useNavigate(); // React Router's navigate function

  const token = "a6c4958b-9dd0-416b-83ab-c484dd771509"; // Use token from local storage or a context if necessary

  const performSearch = async (searchTerm) => {
    if (!searchTerm) return;

    const tickers = [searchTerm.toUpperCase()]; // Convert to uppercase for consistency

    const requestBody = {
      token: token,
      tickers: tickers,
    };

    setLoading(true); // Show loading indicator
    setError(null); // Reset error state

    try {
      // Make the API call and wait for the response
      const response = await fetch('http://localhost:8000/wsb-api/stocks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      setLoading(false); // Hide loading indicator
      const dataString = JSON.stringify(data);
      const commaCount = (dataString.match(/,/g) || []).length;
      console.log('Comma count:', commaCount);

      console.log('API Response:', data); // Log the API response

      // Check if we have a valid ticker
      if (commaCount==26) {
        // Navigate to the stock page if valid data is returned
        console.log('Valid ticker:', searchTerm.toUpperCase());
        navigate(`/stock/${searchTerm.toUpperCase()}`);
      } else {
        // If data is invalid, return to the main page
        console.log('Invalid ticker:', searchTerm.toUpperCase());
        navigate('/'); // Navigate to the main page (root)
      }
    } catch (error) {
      setLoading(false); // Hide loading indicator on error
      setError('There was an error with the fetch operation.');
      console.error('Fetch error:', error);
      navigate('/'); // Return to the main page if an error occurs
    }
  };

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      performSearch(query);
    }
  };

  return (
    <div className="flex items-center space-x-4">
      <div className="relative w-full max-w-xs">
        <input
          type="text"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Search companies or tickers..."
          className="w-full p-2 rounded text-black"
        />
        {loading && <div className="absolute z-20 w-full p-2 text-center">Loading...</div>}
      </div>
    </div>
  );
};

export default SearchBar;
