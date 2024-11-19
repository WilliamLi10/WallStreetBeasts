// CompanyProfile.js
import React, { useState, useEffect } from "react";
import NavBar from "../components/navBar";
import CustomFooter from "../components/customFooter";
import SearchBar from "../components/searchBar";
import { Doughnut, Bar } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";

// Register necessary components for Chart.js
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const StockDisplayPage = () => {
  const [showDoughnut, setShowDoughnut] = useState(true);

  /*
  Work in progress for getting stock data json and reformatting

  useEffect(() => {
    const fetch_stock_data = async () => {
      const back_end_response = await fetch(`wsb-api/stocks/`);
      const company_data_json= await response.json();
    };
  },[]);
  */ 

  const companyData = {
    symbol: "NWP",
    name: "New World Products",
    description:
      "New World Products (NWP) is a leading global company specializing in innovative solutions across various sectors, including renewable energy, technology, and manufacturing. Founded in 1985, NWP has rapidly expanded its operations worldwide and is known for its commitment to sustainability and cutting-edge technology. NWP offers a diverse range of products and services designed to meet the demands of the modern world while ensuring minimal environmental impact.",
    metrics: {
      MarketCapitalization: "75000000000",
      EBITDA: "5600000000",
      EPS: "4.15",
      RevenueTTM: "12000000000",
      BookValue: "35.12",
      ProfitMargin: "0.15",
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
      PERatio: "18.56",
      PEGRatio: "1.22",
      DividendPerShare: "1.25",
      DividendYield: "0.0185",
      RevenuePerShareTTM: "50.85",
      OperatingMarginTTM: "0.20",
      ReturnOnAssetsTTM: "0.08",
      ReturnOnEquityTTM: "0.12",
    },
  };

  // Doughnut Chart Data
  const doughnutData = {
    labels: ["Market Capitalization", "Revenue", "EBITDA"],
    datasets: [
      {
        label: "Financial Overview",
        data: [
          companyData.metrics.MarketCapitalization,
          companyData.metrics.RevenueTTM,
          companyData.metrics.EBITDA,
        ],
        backgroundColor: ["rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)", "rgba(75, 192, 192, 0.6)"],
        borderColor: ["rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)"],
        borderWidth: 1,
      },
    ],
  };

  // Bar Chart Data
  const barData = {
    labels: ["EPS", "Book Value", "Profit Margin (%)"],
    datasets: [
      {
        label: "Performance Metrics",
        data: [
          companyData.metrics.EPS,
          companyData.metrics.BookValue,
          companyData.metrics.ProfitMargin * 100, // Convert to percentage
        ],
        backgroundColor: ["rgba(153, 102, 255, 0.6)", "rgba(255, 159, 64, 0.6)", "rgba(255, 99, 132, 0.6)"],
        borderColor: ["rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)", "rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  };

  const toggleChart = () => setShowDoughnut((prev) => !prev);

  return (
    <div>
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        <NavBar RightComponent={<SearchBar />} />
      </header>
      <main className="container mx-auto px-4 py-12 flex flex-col lg:flex-row gap-12">
        
        {/* Left Section: Company Info and Chart */}
        <div className="lg:w-2/3">
          <h1 className="text-8xl font-bold text-blue-600">{companyData.symbol}</h1>
          <h2 className="text-4xl font-semibold text-gray-800 mt-4">{companyData.name}</h2>
          <p className="mt-6 text-gray-700 leading-relaxed text-xl">{companyData.description}</p>
          <button className="mt-8 text-4xl bg-blue-500 text-white py-4 px-12 rounded-full shadow-lg transition-transform transform hover:scale-105 hover:bg-blue-600">
            Buy Stock
          </button>

          {/* Chart Section */}
          <div className="mt-8 flex flex-col items-center bg-white shadow-md rounded-lg p-4" style={{ height: "500px", maxWidth: "800px" }}>
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">
              {showDoughnut ? "Financial Metrics Distribution" : "Performance Metrics"}
            </h3>
            <div className="w-full flex justify-center" style={{ height: "400px" }}>
              {showDoughnut ? (
                <Doughnut data={doughnutData} options={{ responsive: true, maintainAspectRatio: true }} />
              ) : (
                <Bar data={barData} options={{ responsive: true, maintainAspectRatio: true }} />
              )}
            </div>
            <button
              onClick={toggleChart}
              className="mt-4 text-lg text-blue-500 hover:text-blue-700 transition"
            >
              {showDoughnut ? "→ View Performance Metrics" : "← View Financial Overview"}
            </button>
          </div>
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
