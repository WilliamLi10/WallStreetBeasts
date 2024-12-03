import React from "react";
import logo from "../resources/logo.jpg";
import CustomFooter from '../components/customFooter';

const AboutUs = () => {
  const teamMembers = [
    { name: "Jack Sullivan", role: "Developer" },
    { name: "Sohan Biswal", role: "Developer" },
    { name: "Zach Gestring", role: "Developer" },
    { name: "Nikhil Belgaonkar", role: "Developer" },
    { name: "William Li", role: "Developer" },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 text-gray-800">
      {/* Header */}
      <header className="bg-blue-900 text-white py-8">
        <div className="container mx-auto text-center">
          <img src={logo} alt="Wall Street Beasts Logo" className="mx-auto w-24 mb-4" />
          <h1 className="text-4xl font-bold">About Us</h1>
          <p className="mt-4 text-lg">Empowering investors with insights and tools.</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto py-12 px-4 flex-grow">
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-center mb-6">Our Mission</h2>
          <p className="text-center text-lg max-w-3xl mx-auto">
            At Wall Street Beasts, our goal is to bridge the gap between everyday investors and the stock market.
            We combine cutting-edge technology and expert knowledge to deliver reliable financial tools and insights.
          </p>
        </section>

        <section>
          <h2 className="text-3xl font-bold text-center mb-6">Meet the Team</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8">
            {teamMembers.map((member, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center text-center"
              >
                <div className="w-24 h-24 rounded-full bg-gray-300 flex items-center justify-center text-2xl font-bold text-gray-500 mb-4">
                  {member.name.split(" ").map((n) => n[0]).join("")}
                </div>
                <h3 className="text-xl font-semibold">{member.name}</h3>
                <p className="text-gray-600">{member.role}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <CustomFooter />
    </div>
  );
};

export default AboutUs;
