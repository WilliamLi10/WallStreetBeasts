import React from "react";

const NavBar = ({RightComponent}) => {
  return (
    <nav className="container mx-auto flex justify-between items-center">
      <div className="space-x-8">
        <a href="/news" className="text-white hover:text-gray-300 transition">
          Financial News
        </a>
        <a href="/stocks" className="text-white hover:text-gray-300 transition">
          Investment Insights
        </a>
        <a href="#" className="text-white hover:text-gray-300 transition">
          About Us
        </a>
      </div>
      <div>
        {RightComponent}
      </div>
    </nav>
  );
};

export default NavBar;
