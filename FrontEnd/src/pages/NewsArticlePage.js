import React, { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

const NewsArticlePage = () => {
  const { id } = useParams();
  const location = useLocation();
  const { title, date, author } = location.state || {};
  const [articleContent, setArticleContent] = useState("");

  const mockArticles = {
    1: "Apple releases a groundbreaking phone with advanced AI capabilities.",
    2: "Amazon drones swarm DC for a major announcement on future delivery systems.",
    3: "Mark Zuckerberg defeats Elon Musk in a highly anticipated MMA fight.",
  };

  useEffect(() => {
    // Simulate API call
    const fetchArticleContent = async () => {
      setArticleContent(mockArticles[id] || "Article content not found.");
    };

    fetchArticleContent();
  }, [id, mockArticles]);

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">{title || "News Article"}</h1>
      <p className="text-sm text-gray-600 mb-4">
        {date && `Published on ${date}`} {author && `by ${author}`}
      </p>
      <div className="border-b border-gray-300 mb-4"></div>
      <p className="text-lg text-gray-800 leading-relaxed">{articleContent}</p>
    </div>
  );
};

export default NewsArticlePage;
