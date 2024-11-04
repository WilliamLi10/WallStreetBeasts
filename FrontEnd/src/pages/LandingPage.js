// LandingPage.js
import React from 'react';


import NavBar from "../components/navBar";
import CustomFooter from '../components/customFooter';
import SearchBar from '../components/searchBar';
const LogInAndSignUp = (
  <>
    <a href="#" className="text-white hover:text-gray-300 transition">
      Login
    </a>
    <span className="mx-1 text-gray-300">|</span>
    <a href="#" className="text-white hover:text-gray-300 transition">
      Sign Up
    </a>
  </>
);

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
       <NavBar RightComponent={ <SearchBar />} />
      </header>

      {/* Main content */}
      <main className="container mx-auto py-12 flex justify-between">
        {/* Video section */}
        <div className="w-full h-[500px] md:h-[600px] lg:h-[700px] bg-white shadow-lg p-6 rounded-lg">
        <iframe 
          className="w-full h-[500px] md:h-[600px] rounded-lg shadow-md" 
          src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1" 
          title="YouTube video player" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowFullScreen
       ></iframe>
      </div>

        {/* Get Started Section */}
        <div className="w-1/3 bg-white shadow-lg p-8 rounded-lg flex flex-col place-items-center">
          <button className="bg-yellow-500 text-white py-2 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 hover:bg-yellow-600">
            Get Started
          </button>

          <p className="mt-6 text-gray-600 text-center leading-relaxed">
            Stay ahead in the market with our expert insights. Make informed financial decisions today.
          </p>
        </div>
      </main>

      <CustomFooter />
    </div>
    
  );
};

export default LandingPage;
