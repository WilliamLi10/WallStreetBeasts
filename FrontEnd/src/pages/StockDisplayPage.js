// CompanyProfile.js
import React, { useEffect, useState } from "react";
import NavBar from "../components/navBar";
import CustomFooter from '../components/customFooter';
import SearchBar from '../components/searchBar';
import axios from "axios";

const StockDisplayPage = () => {
  const companyData = {
    symbol: "NWP",
    name: "New World Products",
    description:
      "New World Products (NWP) is a leading global company specializing in innovative solutions across various sectors, including renewable energy, technology, and manufacturing. Founded in 1985, NWP has rapidly expanded its operations worldwide and is known for its commitment to sustainability and cutting-edge technology. NWP offers a diverse range of products and services designed to meet the demands of the modern world while ensuring minimal environmental impact.",
    metrics: {
      AssetType: "Common Stock",
      CIK: "123456",
      Exchange: "NASDAQ",
      Currency: "USD",
      Country: "USA",
      Sector: "Renewable Energy",
      Industry: "Alternative Energy",
      Address: "1234 Green Way, Innovation City, CA, USA",
      FiscalYearEnd: "December",
      LatestQuarter: "2023-06-30",
      MarketCapitalization: "75000000000",
      EBITDA: "5600000000",
      PERatio: "18.56",
      PEGRatio: "1.22",
      BookValue: "35.12",
      DividendPerShare: "1.25",
      DividendYield: "0.0185",
      EPS: "4.15",
      RevenuePerShareTTM: "50.85",
      ProfitMargin: "0.15",
      OperatingMarginTTM: "0.20",
      ReturnOnAssetsTTM: "0.08",
      ReturnOnEquityTTM: "0.12",
      RevenueTTM: "12000000000",
    },
  };

  return (
    <div>
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        <NavBar RightComponent={<SearchBar />} />
      </header>
      <main className="container mx-auto px-4 py-12 flex flex-col lg:flex-row gap-12">
        {/* Left Section: Company Info */}
        <div className="lg:w-2/3">
          <h1 className="text-8xl font-bold text-blue-600">
            {companyData.symbol}
          </h1>
          <h2 className="text-4xl font-semibold text-gray-800 mt-4">
            {companyData.name}
          </h2>
          <p className="mt-6 text-gray-700 leading-relaxed text-xl">
            {companyData.description}
          </p>
          <button className="mt-8 text-4xl bg-blue-500 text-white py-4 px-12 rounded-full shadow-lg transition-transform transform hover:scale-105 hover:bg-blue-600">
            Buy Stock
          </button>
        </div>

        {/* Right Section: Data Table */}
        <div className="lg:w-1/3">
          <div className="bg-white shadow-md rounded-lg p-4">
            <table className="w-full text-sm text-left text-gray-700">
              <tbody>
                {Object.entries(companyData.metrics).map(([key, value]) => (
                  <tr key={key}>
                    <td className="py-2 font-semibold capitalize">{key}</td>
                    <td className="py-2">{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
      <CustomFooter />
    </div>
  );
};

export default StockDisplayPage;
