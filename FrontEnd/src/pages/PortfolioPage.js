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
import { Link } from "react-router-dom";
import axios from "axios";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const PortfolioPage = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);

  const [updates] = useState([
    { title: "Apple New Phone Release", description: "Apple releases new phone today..." },
    { title: "Amazon Drones Attack DC", description: "The supreme court was attacked..." },
    { title: "Zuckerberg Chokes Out Musk", description: "Mark Zuckerberg wins by Sub..." },
  ]);

  // Fetch portfolio data
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
        // Process this data to get detailed information about each stock

        const portfolioDetails = await Promise.all(
          data.portfolio.map(async (item) => {
            const [symbol, quantity] = item.split(":");
            const qty = parseInt(quantity) || 0;

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
          updates: updates,
        });
      } catch (error) {
        console.error("Error fetching portfolio data:", error);
      }
    };

    fetchData();
  }, [updates]);

  // Function to remove stock from portfolio
  const removeStockFromPortfolio = async (stock) => {
    const token = document.cookie.split("; ").find((row) => row.startsWith("token="))?.split("=")[1];
    if (!token) {
      alert("You must be logged in to perform this action.");
      return;
    }
    console.log(stock.name)
    try {
      // Send the request to remove the stock
      const response = await axios.post("http://localhost:8000/wsb-api/edit_portfolio/", {
        token,
        add: [],
        remove: [`${stock.name}`] // Dynamically passing the stock ticker to remove
        
      });
  
      alert(response.data.message); // Show success message from API
      // Update the portfolio data locally by filtering out the removed stock
      setPortfolioData((prevState) => {
        const updatedPortfolio = prevState.portfolio.filter(
          (item) => item.name !== stock.name
        );
        return { ...prevState, portfolio: updatedPortfolio };
      });
  
    } catch (error) {
      console.error("Error removing stock from portfolio:", error);
      alert("Failed to remove stock from portfolio. Please try again.");
    }
  };
  

  const analyzePortfolio = async () => {
    try {
      if (!portfolioData || !portfolioData.portfolio) {
        console.error("Portfolio data is not available");
        return;
      }

      const tickers = portfolioData.portfolio.map((stock) => stock.name);

      const response = await axios.post("http://localhost:8000/wsb-api/analyze-portfolio/", {
        tickers,
      });

      const data = response.data;
      setAnalysisResults(data);
      setIsModalOpen(true);
    } catch (error) {
      console.error("Error analyzing portfolio:", error);
      alert("Failed to analyze portfolio. Please try again.");
    }
  };

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
            {selectedStock ? (
              <Link to={`/stock/${selectedStock.name}`} className="text-blue-500 hover:underline">
                {`${selectedStock.name} Performance`}
              </Link>
            ) : (
              "Portfolio Performance"
            )}
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
                <th className="py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map((stock, index) => (
                <tr key={index} className="border-b hover:bg-gray-100">
                  <td className="py-2">{stock.name}</td>
                  <td className="py-2">{stock.total}</td>
                  <td className="py-2">{stock.price}</td>
                  <td className="py-2">{stock.allocation}</td>
                  <td className="py-2">
                    <button
                      onClick={() => removeStockFromPortfolio(stock)}
                      className="text-red-500 hover:text-red-700"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>

      {/* Modal for Analysis Results */}
      {isModalOpen && analysisResults && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-3/4 max-h-full overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Portfolio Analysis</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-lg">Overall Growth</h3>
                <p className="text-gray-700">{analysisResults.overallGrowth}</p>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Top Performers</h3>
                <ul className="list-disc list-inside text-gray-700">
                  {analysisResults.topPerformers.map((stock, index) => (
                    <li key={index}>{`${stock.name}: ${stock.growth}`}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Recommendations</h3>
                <ul className="list-disc list-inside text-gray-700">
                  {analysisResults.recommendations.map((rec, index) => (
                    <li key={index}>
                      {`${rec.action} ${rec.stock} - ${rec.reason}`}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="flex justify-end mt-4">
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                onClick={() => setIsModalOpen(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      <CustomFooter />
    </div>
  );
};

export default PortfolioPage;
