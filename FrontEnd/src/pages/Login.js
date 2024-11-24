import React, { useState } from 'react';
import { Redirect } from 'react-router';


const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({email: email, password: password})
    // need to store login code in cookie named token
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Request options:', requestOptions);
    fetch('http://localhost:8000/wsb-api/login/', requestOptions)
      .then(response => {
      if (response.ok) {
        // Parse the JSON response
        console.log("There was a response", response);
        return (<Redirect to='http://localhost:8000/wsb-api/portfolio/' />);
        //return response.json();
      } else {
        throw new Error('Network response was not ok');
      }    
    })
    .then(data => {
      // Handle the data returned from the server
      console.log('Post request response:', data);
    })
    .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('There was a problem with the fetch operation:', error);
    });
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-800">Login</h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-600">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-gray-700 bg-gray-200 border rounded focus:outline-none focus:ring focus:border-blue-300"
              placeholder="Enter your email"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-600">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-gray-700 bg-gray-200 border rounded focus:outline-none focus:ring focus:border-blue-300"
              placeholder="Enter your password"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 font-semibold text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring focus:bg-blue-700"
          >
            Login
          </button>
        </form>
        <p className="text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/signup" className="font-semibold text-blue-600 hover:underline">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
