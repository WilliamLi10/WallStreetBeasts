import React from "react";
import { isLoggedIn } from "../resources/auth";
import { useNavigate } from "react-router-dom";

const NavBar = ({ RightComponent }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear the token cookie
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    // Redirect to the home page
    navigate("/");
  };

  return (
    <nav className="container mx-auto flex justify-between items-center py-4">
      <div className="space-x-8">
        <a href="/" className="text-white hover:text-gray-300 transition">
          Home
        </a>
        <a href="/news" className="text-white hover:text-gray-300 transition">
          Financial News
        </a>
        <a href="/portfolio" className="text-white hover:text-gray-300 transition">
          Portfolio
        </a>
        <a href="/aboutus" className="text-white hover:text-gray-300 transition">
          About Us
        </a>
      </div>
      <div>
        {isLoggedIn() ? (
          <button
            onClick={handleLogout}
            className="bg-red-500 px-4 py-2 rounded text-white hover:bg-red-600 transition"
          >
            Logout
          </button>
        ) : (
          RightComponent
        )}
      </div>
    </nav>
  );
};

export default NavBar;
