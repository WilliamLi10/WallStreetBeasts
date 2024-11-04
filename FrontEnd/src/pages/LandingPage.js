import React from 'react';
import NavBar from "../components/navBar";
import CustomFooter from '../components/customFooter';
import SearchBar from '../components/searchBar';
import LogInAndSignUp from '../components/LogInAndSignUp';

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Navbar */}
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        <NavBar RightComponent={
          <div className="flex items-center space-x-4">
            <SearchBar />
            <LogInAndSignUp />
          </div>
        } />
      </header>

      {/* Main content */}
      <main className="container mx-auto py-12 flex-grow flex flex-col lg:flex-row lg:justify-between items-center space-y-6 lg:space-y-0 lg:space-x-6">
        
        {/* Video section */}
        <div className="w-full lg:w-2/3 bg-white shadow-lg p-6 rounded-lg">
          <iframe 
            className="w-full h-[300px] md:h-[400px] lg:h-[500px] rounded-lg shadow-md" 
            src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1" 
            title="YouTube video player" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowFullScreen
          ></iframe>
        </div>

        {/* Get Started Section */}
        <div className="w-full lg:w-1/3 bg-white shadow-lg p-8 rounded-lg flex flex-col items-center text-center">
          <a href='Login'>
          <button className="bg-yellow-500 text-white py-2 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 hover:bg-yellow-600">
            Get Started
          </button>
          </a>
          

          <p className="mt-6 text-gray-600 leading-relaxed">
            Stay ahead in the market with our expert insights. Make informed financial decisions today.
          </p>
        </div>
      </main>

      {/* Footer */}
      <CustomFooter />
    </div>
  );
};

export default LandingPage;
