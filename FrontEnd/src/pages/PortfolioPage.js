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

  const [mockData] = useState({
    chart: {
      labels: ["January", "February", "March", "April", "May"],
      datasets: [
        {
          label: "Portfolio Performance",
          data: [10000, 15000, 12000, 18000, 20000],
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 2,
        },
      ],
    },
    portfolio: [
      {
        name: "AAPL",
        total: "$10,000",
        price: "$227.5/Share",
        allocation: "27.5%",
        chart: {
          labels: ["January", "February", "March", "April", "May"],
          datasets: [
            {
              label: "AAPL Performance",
              data: [120, 130, 125, 140, 150],
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 2,
            },
          ],
        },
      },
      {
        name: "AMZN",
        total: "$15,000",
        price: "$188.7/Share",
        allocation: "34%",
        chart: {
          labels: ["January", "February", "March", "April", "May"],
          datasets: [
            {
              label: "AMZN Performance",
              data: [200, 210, 220, 230, 240],
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 2,
            },
          ],
        },
      },
      {
        name: "META",
        total: "$10,000",
        price: "$589.3/Share",
        allocation: "27.5%",
        chart: {
          labels: ["January", "February", "March", "April", "May"],
          datasets: [
            {
              label: "META Performance",
              data: [300, 320, 310, 330, 340],
              backgroundColor: "rgba(255, 206, 86, 0.2)",
              borderColor: "rgba(255, 206, 86, 1)",
              borderWidth: 2,
            },
          ],
        },
      },
      {
        name: "DKNG",
        total: "$10,000",
        price: "$227.5/Share",
        allocation: "27.5%",
        chart: {
          labels: ["January", "February", "March", "April", "May"],
          datasets: [
            {
              label: "DKNG Performance",
              data: [90, 100, 95, 110, 120],
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 2,
            },
          ],
        },
      },
    ],
    updates: [
      { title: "Apple New Phone Release", description: "Apple releases new phone today..." },
      { title: "Amazon Drones Attack DC", description: "The supreme court was attacked..." },
      { title: "Zuckerberg Chokes Out Musk", description: "Mark Zuckerberg wins by Sub..." },
    ],
  });
  

  // Fetch portfolio data (mocked initially)
  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      try {
        // Uncomment the below code when backend is ready
        // const response = await fetch("https://your-backend-api/portfolio");
        // const data = await response.json();
        // setPortfolioData(data);

        // Use mock data for now
        setPortfolioData(mockData);
      } catch (error) {
        console.error("Error fetching portfolio data:", error);
      }
    };

    fetchData();
  }, [mockData]);

  if (!portfolioData) {
    return <div className="text-center py-10">Loading...</div>;
  }

  const { chart, portfolio, updates } = portfolioData;

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
