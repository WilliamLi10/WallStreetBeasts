// LandingPage.js
import React from 'react';
import logo from './logo.jpg';


const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        <nav className="container mx-auto flex justify-between items-center">
          <div className="space-x-8">
            <a href="#" className="text-white hover:text-gray-300 transition">Financial News</a>
            <a href="#" className="text-white hover:text-gray-300 transition">Investment Insights</a>
            <a href="#" className="text-white hover:text-gray-300 transition">About Us</a>
          </div>
          <div>
            <a href="#" className="text-white hover:text-gray-300 transition">Login</a>
            <span className="mx-1 text-gray-300">|</span>
            <a href="#" className="text-white hover:text-gray-300 transition">Sign Up</a>
          </div>
        </nav>
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
      

      <footer className="fixed bottom-0 left-0 z-20 w-full p-4 bg-white border-t border-gray-200 shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800 dark:border-gray-600">
         <a href="localhost:3000" className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse">
            <img src={logo} className="h-8" alt="Our Logo" />
           <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Wall Street Beasts</span>
        </a>
        <ul className="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
         <li>
              <a href="#" className="hover:underline me-4 md:me-6">About</a>
          </li>
          <li>
              <a href="#" className="hover:underline">Contact</a>
          </li>
        </ul>
      </footer>

    </div>
    
  );
};

export default LandingPage;
