import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  // State variables
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate(); // Initialize navigate function

  const handleSubmit = (e) => {
    e.preventDefault();

    // Check if passwords match
    if (password !== confirmPassword) {
      console.error('Passwords do not match');
      // Optionally, set an error message state to display to the user
      return;
    }

    const registerOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    };

    // Register the user
    fetch('http://localhost:8000/wsb-api/register/', registerOptions)
      .then(response => {
        if (response.ok) {
          console.log('Registration successful');

          // Prepare login request
          const loginOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          };

          // Log the user in
          return fetch('http://localhost:8000/wsb-api/login/', loginOptions);
        } else {
          throw new Error('Registration failed');
        }
      })
      .then(response => {
        if (response.ok) {
          console.log('Login successful');
          return response.json();
        } else {
          throw new Error('Login failed');
        }
      })
      .then(data => {
        // Store the login token in a cookie
        document.cookie = `token=${data.token}; path=/;`;

        // Navigate to the portfolio page
        navigate('/portfolio/');
      })
      .catch(error => {
        console.error('Error:', error);
        // Optionally, set an error message state to display to the user
      });
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-800">
          Sign Up
        </h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-gray-600">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600"
              required
            />
          </div>

          <div>
            <label className="block text-gray-600">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600"
              required
            />
          </div>

          <div>
            <label className="block text-gray-600">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600"
              required
            />
          </div>

          <div>
            <label className="block text-gray-600">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 mt-4 font-semibold text-white transition-transform transform bg-blue-600 rounded-full shadow-lg hover:scale-105 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            Sign Up
          </button>
        </form>

        <p className="mt-4 text-center text-gray-600">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 hover:underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
