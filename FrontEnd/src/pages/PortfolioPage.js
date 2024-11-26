import React, { useEffect, useState } from "react";
import NavBar from "../components/navBar";
import CustomFooter from "../components/customFooter";
import SearchBar from "../components/searchBar";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const PortfolioPage = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);

  const [updates] = useState([
    { title: "Apple New Phone Release", description: "Apple releases new phone today..." },
    { title: "Amazon Drones Attack DC", description: "The supreme court was attacked..." },
    { title: "Zuckerberg Chokes Out Musk", description: "Mark Zuckerberg wins by Sub..." },
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get the token from the cookies
        const token = document.cookie
          .split("; ")
          .find((row) => row.startsWith("token="))
          ?.split("=")[1];

        if (!token) {
          console.error("No token found in cookies");
          return;
        }

        // Fetch the portfolio data from the backend
        const response = await fetch("http://localhost:8000/wsb-api/portfolio/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ token }),
        });

        if (!response.ok) {
          throw new Error("Failed to fetch portfolio data");
        }

        const data = await response.json();
        console.log("Portfolio data received:", data);

        // Assuming data.portfolio is an array of strings like ["AAPL:10", "AMZN:15"]
        // We need to process this data to get detailed information about each stock

        // For each stock in the portfolio, fetch additional details
        const portfolioDetails = await Promise.all(
          data.portfolio.map(async (item) => {
            const [symbol, quantity] = item.split(":");
            const qty = parseInt(quantity) || 0;

            // Fetch stock details from an API
            // Replace 'your_stock_api_endpoint' with your actual endpoint
            // For now, we'll use placeholder data

            // Placeholder stock details
            const stockDetails = {
              name: symbol,
              total: `$${(qty * 100).toFixed(2)}`, // Placeholder total value
              price: `$100/Share`, // Placeholder price
              allocation: "25%", // Placeholder allocation
              chart: {
                labels: ["January", "February", "March", "April", "May"],
                datasets: [
                  {
                    label: `${symbol} Performance`,
                    data: [100, 110, 105, 115, 120], // Placeholder data
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 2,
                  },
                ],
              },
            };
            return stockDetails;
          })
        );

        // Create overall portfolio chart data
        const chartData = {
          labels: ["January", "February", "March", "April", "May"],
          datasets: [
            {
              label: "Portfolio Performance",
              data: [10000, 15000, 12000, 18000, 20000], // Placeholder data
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 2,
            },
          ],
        };

        setPortfolioData({
          chart: chartData,
          portfolio: portfolioDetails,
          updates: updates, // Keep updates as mock data
        });
      } catch (error) {
        console.error("Error fetching portfolio data:", error);
      }
    };

    fetchData();
  }, [updates]);

  if (!portfolioData) {
    return <div className="text-center py-10">Loading...</div>;
  }

  const { chart, portfolio } = portfolioData;

  return (
    <div>
      <header className="bg-gradient-to-r from-blue-900 via-blue-800 to-blue-600 text-white py-4">
        <NavBar RightComponent={<SearchBar />} />
      </header>
      <main className="container mx-auto px-4 py-12 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Section: Chart */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">
            {selectedStock ? `${selectedStock.name} Performance` : "Portfolio Performance"}
          </h2>
          <Line
            data={selectedStock ? selectedStock.chart : chart}
            options={{ responsive: true, maintainAspectRatio: true }}
          />
        </div>

        {/* Right Section: Updates */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Updates</h2>
          {updates.map((update, index) => (
            <div
              key={index}
              className="border-b border-gray-300 pb-4 mb-4 last:border-0 last:pb-0 last:mb-0"
            >
              <h3 className="font-semibold text-gray-800">{update.title}</h3>
              <p className="text-sm text-gray-600">{update.description}</p>
            </div>
          ))}
        </div>

        {/* Bottom Section: Portfolio Table */}
        <div className="col-span-3 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Portfolio Allocation</h2>
          <table className="w-full text-left text-sm text-gray-700">
            <thead className="border-b">
              <tr>
                <th className="py-2">Name</th>
                <th className="py-2">Total</th>
                <th className="py-2">Price</th>
                <th className="py-2">Allocation</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map((stock, index) => (
                <tr
                  key={index}
                  className={`cursor-pointer ${index % 2 === 0 ? "bg-gray-50" : ""}`}
                  onClick={() => setSelectedStock(stock)}
                >
                  <td className="py-2">{stock.name}</td>
                  <td className="py-2">{stock.total || "N/A"}</td>
                  <td className="py-2">{stock.price || "N/A"}</td>
                  <td className="py-2">{stock.allocation || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
      <CustomFooter />
    </div>
  );
};

export default PortfolioPage;
