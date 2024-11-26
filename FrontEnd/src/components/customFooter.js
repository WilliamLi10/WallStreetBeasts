import React from "react";
import logo from "../resources/logo.jpg";
const CustomFooter = () => {
  return (
    <footer className="w-full p-4 bg-white border-t border-gray-200 shadow md:flex md:items-center md:justify-between md:p-6 dark:bg-gray-800 dark:border-gray-600">
      <a
        href="/"
        className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse"
      >
        <img src={logo} className="h-8" alt="Our Logo" />
        <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">
          Wall Street Beasts
        </span>
      </a>
      <ul className="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
          <a href="/aboutus" className="hover:underline me-4 md:me-6">
            About
          </a>
        </li>
        <li>
          <a href="#" className="hover:underline">
            Contact
          </a>
        </li>
      </ul>
    </footer>
  );
};

export default CustomFooter;
