import React, { useState } from 'react';
import { Redirect } from 'react-router';


const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({username: username, email:email, password: password})
    // need to store login code in cookie named token
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:8000/wsb-api/register/', requestOptions)
      .then(response => {
      if (response.ok) {
        console.log("There was a response (sign up)", response);
        fetch('http://localhost:8000/wsb-api/login/', requestOptions)
          .then(response => {
          if (response.ok) {
            console.log("There was a response (log in)", response);
            return (<Redirect to='http://localhost:8000/wsb-api/portfolio/' />);
            //return response.json();
          } else {
            throw new Error('Network response was not ok (log in)');
          }
        })
        .then(data => {
          // Handle the data returned from the server
          console.log('Post request response (log in):', data);
        })
        .catch(error => {
          // Handle any errors that occurred during the fetch
          console.error('There was a problem with the fetch operation (log in):', error);
        });
        //return response.json();
      } else {
        throw new Error('Network response was not ok (sign up)');
      }
    })
    .then(data => {
      // Handle the data returned from the server
      console.log('Post request response (sign up):', data);
    })
    .catch(error => {
      // Handle any errors that occurred during the fetch
      console.error('There was a problem with the fetch operation (sign up):', error);
    });
    console.log('Username:', username);
    console.log('Email:', email);
    console.log('Password:', password);
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
          <a href="/Login" className="text-blue-600 hover:underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
