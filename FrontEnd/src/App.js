// App.js
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import StockDisplayPage from "./pages/StockDisplayPage";
import Login from "./pages/Login";
import PortfolioPage from "./pages/PortfolioPage";
import Signup from "./pages/Signup";
import Error from "./components/Error";
import NewsPage from "./pages/NewsPage"; // Import the NewsPage component
import "tailwindcss/tailwind.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />,
    errorElement: <Error />,
  },
  {
    path: "/stocks",
    element: <StockDisplayPage />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/Signup",
    element: <Signup />,
  },
  {
    path: "/Portfolio",
    element: <PortfolioPage />
  },
  {
    path: "/news", // Add the NewsPage route
    element: <NewsPage />,
  },

]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
