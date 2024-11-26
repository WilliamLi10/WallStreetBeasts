import React, { useEffect, useState } from "react";
import NavBar from "../components/navBar";
import CustomFooter from "../components/customFooter";
import SearchBar from "../components/searchBar";
import axios from "axios";
import LogInAndSignUp from '../components/LogInAndSignUp';

import "./NewsPage.css";  // Import the custom CSS for scrolling animation

const NewsPage = () => {
  const [articles, setArticles] = useState([]);  // Initialize as an empty array
  const [trendingStocks, setTrendingStocks] = useState([]); // New state for stocks
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isPaused, setIsPaused] = useState(false); // Pause state for scrolling

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Replace with your actual API URL
        const response = await axios.get("http://localhost:8000/wsb-api/home/");

        // Validate and update the state with the correct response data
        if (response.data.news && Array.isArray(response.data.news)) {
          setArticles(response.data.news);  // Update news
        } else {
          throw new Error("API response is not in the expected format");
        }

        if (response.data.trending_stocks && Array.isArray(response.data.trending_stocks.data)) {
          setTrendingStocks(response.data.trending_stocks.data);  // Update trending stocks
        } else {
          throw new Error("Trending stocks data is not in the expected format");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Failed to load data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handlePauseResume = () => {
    setIsPaused((prevState) => !prevState); // Toggle the paused state
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
      <main className="container mx-auto px-4 py-12">
        <h1 className="text-6xl font-bold text-blue-600 mb-8">Latest News and Trending Stocks</h1>
        {loading ? (
          <p className="text-xl text-gray-700">Loading articles...</p>
        ) : error ? (
          <p className="text-xl text-red-500">{error}</p>
        ) : (
          <>
            {/* Rotating Stocks Wheel */}
            <div className="overflow-hidden relative mb-12">
              <div className={`stock-container ${isPaused ? "paused" : ""}`}>
                {trendingStocks.map((stock, index) => (
                  <div
                    key={index}
                    className="stock-item flex items-center justify-center w-1/3 px-4 text-white text-xl font-semibold"
                  >
                    <span className="mr-2">{stock[0]}</span>
                    <span className="text-sm">Volume: {stock[1].toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* News container with continuous scroll */}
            <div className="overflow-hidden relative">
              <div className={`news-container ${isPaused ? "paused" : ""}`}>
                {articles.map((article) => (
                  <div
                    key={article.id}
                    className="w-full flex-shrink-0 p-4 bg-white shadow-md rounded-lg mr-4"
                  >
                    <img
                      src={article.image}
                      alt={article.headline}
                      className="w-full h-48 object-cover rounded-md mb-4"
                    />
                    <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                      {article.headline}
                    </h2>
                    <p className="text-gray-600 mb-4">{article.summary}</p>
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:underline"
                    >
                      Read more
                    </a>
                    <p className="mt-4 text-sm text-gray-500">Source: {article.source}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
        {/* Pause/Resume Button */}
        <button
          onClick={handlePauseResume}
          className="mt-6 p-2 bg-blue-500 text-white rounded-lg"
        >
          {isPaused ? "Resume Scrolling" : "Pause Scrolling"}
        </button>
      </main>
      <CustomFooter />
    </div>
  );
};

export default NewsPage;
