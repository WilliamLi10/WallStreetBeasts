import React, { useState } from "react";


const UserSettings = () => {
  // State for password recovery
  const [emailForRecovery, setEmailForRecovery] = useState("");
  const [recoveryMessage, setRecoveryMessage] = useState("");

  // State for changing email
  const [newEmail, setNewEmail] = useState("");
  const [confirmNewEmail, setConfirmNewEmail] = useState("");
  const [emailChangeMessage, setEmailChangeMessage] = useState("");

  // Handle password recovery form submission
  const handlePasswordRecovery = (e) => {
    e.preventDefault();
    if (emailForRecovery) {
      setRecoveryMessage("Password recovery instructions have been sent to your email.");
    } else {
      setRecoveryMessage("Please enter a valid email address.");
    }
  };

  // Handle email change form submission
  const handleEmailChange = (e) => {
    e.preventDefault();
    if (newEmail === confirmNewEmail) {
      setEmailChangeMessage("Your email address has been successfully updated.");
    } else {
      setEmailChangeMessage("Email addresses do not match. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6">User Settings</h1>
        <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        
      </header>

        {/* Password Recovery Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Recover Password</h2>
          <form onSubmit={handlePasswordRecovery} className="space-y-4">
            <div>
              <label htmlFor="emailForRecovery" className="block text-gray-700 font-medium mb-2">
                Enter Your Email
              </label>
              <input
                type="email"
                id="emailForRecovery"
                value={emailForRecovery}
                onChange={(e) => setEmailForRecovery(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
                placeholder="Enter your email"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition"
            >
              Recover Password
            </button>
          </form>
          {recoveryMessage && (
            <p className="mt-4 text-center text-gray-600">{recoveryMessage}</p>
          )}
        </div>

        {/* Change Email Section */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Change Email Address</h2>
          <form onSubmit={handleEmailChange} className="space-y-4">
            <div>
              <label htmlFor="newEmail" className="block text-gray-700 font-medium mb-2">
                New Email Address
              </label>
              <input
                type="email"
                id="newEmail"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
                placeholder="Enter new email"
                required
              />
            </div>
            <div>
              <label htmlFor="confirmNewEmail" className="block text-gray-700 font-medium mb-2">
                Confirm New Email Address
              </label>
              <input
                type="email"
                id="confirmNewEmail"
                value={confirmNewEmail}
                onChange={(e) => setConfirmNewEmail(e.target.value)}
                className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"
                placeholder="Confirm new email"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-green-600 text-white font-semibold rounded hover:bg-green-700 transition"
            >
              Change Email Address
            </button>
          </form>
          {emailChangeMessage && (
            <p className="mt-4 text-center text-gray-600">{emailChangeMessage}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserSettings;
