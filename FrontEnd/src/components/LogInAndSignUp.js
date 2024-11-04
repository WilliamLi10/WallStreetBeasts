import React from "react";

const LogInAndSignUp = () => {
  return (
    <>
      <a href="Login" className="text-white hover:text-gray-300 transition">
        Login
      </a>
      <span className="mx-1 text-gray-300">|</span>
      <a href="/Signup" className="text-white hover:text-gray-300 transition">
        Sign Up
      </a>
    </>
  );
};

export default LogInAndSignUp;

