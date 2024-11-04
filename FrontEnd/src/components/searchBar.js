import React, { useState, useCallback } from 'react';
import debounce from 'lodash.debounce';

// Mock data starting with letter 'A'
const mockData = [
  { name: 'Apple Inc.', ticker: 'AAPL' },
  { name: 'Amazon.com, Inc.', ticker: 'AMZN' },
  { name: 'Alphabet Inc.', ticker: 'GOOGL' },
  { name: 'Adobe Inc.', ticker: 'ADBE' },
  { name: 'Advanced Micro Devices, Inc.', ticker: 'AMD' },
  { name: 'American Airlines Group Inc.', ticker: 'AAL' },
  { name: 'Activision Blizzard, Inc.', ticker: 'ATVI' },
  { name: 'Autodesk, Inc.', ticker: 'ADSK' },
  { name: 'Analog Devices, Inc.', ticker: 'ADI' },
  { name: 'Airbnb, Inc.', ticker: 'ABNB' },
];


const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const autocompleteEnabled = true; // You can set this as needed

  const fetchSuggestions = useCallback(
    debounce((searchTerm) => {
      if (searchTerm.trim() === '') {
        setSuggestions([]);
        return;
      }
      // Filter mock data based on the search term
      const filteredData = mockData.filter((item) =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.ticker.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setSuggestions(filteredData);
    }, 300),
    []
  );

  // Handle input change
  const handleChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    if (autocompleteEnabled) {
      fetchSuggestions(value);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      performSearch(query);
    }
  };

  const performSearch = (searchTerm) => {
    const results = mockData.filter((item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.ticker.toLowerCase().includes(searchTerm.toLowerCase())
    );
    console.log('Search results:', results);
    // Handle the results as needed (e.g., display them or navigate)
  };

  return (
    <div className="flex items-center space-x-4">
      {/* Search Input */}
      <div className="relative w-full max-w-xs">
        <input
          type="text"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Search companies or tickers..."
          className="w-full p-2 rounded text-black"
        />
        {autocompleteEnabled && suggestions.length > 0 && (
          <ul className="absolute z-10 w-full bg-white border rounded shadow">
            {suggestions.map((item, index) => (
              <li key={index} className="p-2 hover:bg-gray-100 cursor-pointer text-black">
                {item.name} ({item.ticker})
              </li>
            ))}
          </ul>
        )}
      </div>

  
    </div>
  );
};

export default SearchBar;
