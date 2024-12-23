import React, { useState, useEffect } from "react";
import NavBar from "../components/navBar";
import CustomFooter from "../components/customFooter";
import SearchBar from "../components/searchBar";
import { Doughnut, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import axios from "axios";
import { useParams } from "react-router-dom";
import LogInAndSignUp from '../components/LogInAndSignUp';

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const StockDisplayPage = () => {
  const { ticker } = useParams(); // Get the stock ticker from URL parameters
  const [companyData, setCompanyData] = useState(null);
  const [showDoughnut, setShowDoughnut] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [stockQuantity, setStockQuantity] = useState(0);
  const [currentPrice, setCurrentPrice] = useState(null);
  const [loadingPrice, setLoadingPrice] = useState(false);

  useEffect(() => {
    const fetchCompanyData = async () => {
      try {
        // Prepare the request payload
        const requestData = {
          tickers: [ticker],
        };

        // Make the API call to fetch stock data
        const response = await axios.post("http://localhost:8000/wsb-api/stocks/", requestData);

        // Parse the response data
        let data = response.data;
        if (typeof data === "string") {
          data = JSON.parse(data);
        }

        // Check if data for the ticker is available
        const upperTicker = ticker.toUpperCase(); // Ensure ticker is in uppercase
        console.log(upperTicker);
        console.log(data[upperTicker]);
        if (data[upperTicker]) {
          setCompanyData(data[upperTicker]);
          setCurrentPrice(data["Current Price"]);
        } else {
          alert("Stock data not found for the ticker: " + ticker);
        }
      } catch (error) {
        console.error("Error fetching company data:", error);
        alert("Failed to fetch company data. Please try again.");
      }
    };

    fetchCompanyData();
  }, [ticker]);

  const openModal = async () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setStockQuantity(0);
  };

  const handleBuyStock = async () => {
    const token = document.cookie.split("; ").find((row) => row.startsWith("token="))?.split("=")[1];
    if (!token) {
      alert("You must be logged in to perform this action.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/wsb-api/edit_portfolio/", {
        add: [`${companyData.ticker}:${stockQuantity}`],
        remove: [],
        token,
      });
      alert(response.data.message);
      closeModal();
    } catch (error) {
      console.error("Error updating portfolio:", error);
      alert("Failed to update portfolio. Please try again.");
    }
  };

  const toggleChart = () => setShowDoughnut((prev) => !prev);

  if (!companyData) {
    return <div className="text-center py-10">Loading...</div>;
  }

  // Prepare chart data using companyData
  const doughnutData = {
    labels: ["Current Price", "Target Price", "Free Cash Flow (B)"],
    datasets: [
      {
        label: "Financial Overview",
        data: [
          parseFloat(companyData.current_price.replace("$", "")),
          parseFloat(companyData.target_price.replace("$", "")),
          parseFloat(companyData.free_cash_flow.replace("$", "").replace("B", "")),
        ],
        backgroundColor: ["rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)", "rgba(75, 192, 192, 0.6)"],
        borderColor: ["rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)"],
        borderWidth: 1,
      },
    ],
  };

  const barData = {
    labels: ["PE Ratio", "Growth Potential (%)", "Beta"],
    datasets: [
      {
        label: "Performance Metrics",
        data: [
          parseFloat(companyData.pe_ratio),
          parseFloat(companyData.growth_potential.replace("%", "")),
          parseFloat(companyData.beta),
        ],
        backgroundColor: ["rgba(153, 102, 255, 0.6)", "rgba(255, 159, 64, 0.6)", "rgba(255, 99, 132, 0.6)"],
        borderColor: ["rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)", "rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
      <NavBar RightComponent={
          <div className="flex items-center space-x-4">
            <SearchBar />
            <LogInAndSignUp />
          </div>
        } />
      </header>
      <main className="container mx-auto px-4 py-12 flex flex-col lg:flex-row gap-12">
        {/* Left Section: Company Info and Chart */}
        <div className="lg:w-2/3">
          <h1 className="text-8xl font-bold text-blue-600">{companyData.ticker}</h1>
          <h2 className="text-4xl font-semibold text-gray-800 mt-4">{companyData.industry}</h2>
          <p className="mt-6 text-gray-700 leading-relaxed text-xl">
            Recommendation: <strong>{companyData.recommendation}</strong> (Score: {companyData.score})
          </p>
          <button
            className="mt-8 text-4xl bg-blue-500 text-white py-4 px-12 rounded-full shadow-lg transition-transform transform hover:scale-105 hover:bg-blue-600"
            onClick={openModal}
          >
            Buy Stock
          </button>
          <div
            className="mt-8 flex flex-col items-center bg-white shadow-md rounded-lg p-4"
            style={{ height: "500px", maxWidth: "800px" }}
          >
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
            <button onClick={toggleChart} className="mt-4 text-lg text-blue-500 hover:text-blue-700 transition">
              {showDoughnut ? "→ View Performance Metrics" : "← View Financial Overview"}
            </button>
          </div>
        </div>

        {/* Right Section: Data Table */}
        <div className="lg:w-1/3">
          <div className="bg-white shadow-md rounded-lg p-4">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">Company Metrics</h3>
            <table className="w-full text-sm text-left text-gray-700 border border-gray-200 rounded">
              <tbody>
                {Object.entries(companyData).map(([key, value]) => (
                  <tr key={key} className="border-b border-gray-200">
                    <td className="py-2 font-semibold capitalize text-gray-800">
                      {key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                    </td>
                    <td className="py-2 text-gray-600">{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
      {isModalOpen && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-8 w-1/3">
            <h2 className="text-xl font-bold mb-4">Buy Stock: {companyData.ticker}</h2>
            <p className="mb-4">
              {loadingPrice
                ? "Loading price..."
                : `Current Price: ${companyData.current_price}/Share`}
            </p>
            <label className="block mb-4">
              <span className="text-gray-700">Quantity</span>
              <input
                type="number"
                value={stockQuantity}
                onChange={(e) => setStockQuantity(e.target.value)}
                className="block w-full mt-2 border border-gray-300 rounded py-2 px-4"
                placeholder="Enter quantity"
                min="1"
              />
            </label>
            <div className="flex justify-end gap-4">
              <button
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                onClick={closeModal}
              >
                Cancel
              </button>
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                onClick={handleBuyStock}
                disabled={loadingPrice || stockQuantity <= 0}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
      <CustomFooter />
    </div>
  );
};

export default StockDisplayPage;
