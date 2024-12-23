import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import StockDisplayPage from "./pages/StockDisplayPage";
import Login from "./pages/Login";
import PortfolioPage from "./pages/PortfolioPage";
import Signup from "./pages/Signup";
import Error from "./components/Error";
import NewsPage from "./pages/NewsPage"; // Import the NewsPage component
import AboutUs from "./pages/AboutUs";
import UserSettings from "./pages/UserSettings";
import "tailwindcss/tailwind.css";
import ProtectedRoute from "./components/protectedRoute";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />,
    errorElement: <Error />,
  },
  {
    path: "/stock/:ticker", // Update to dynamic route for StockDisplayPage
    element: <StockDisplayPage />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <Signup />,
  },
  {
    path: "/portfolio",
    element:<ProtectedRoute><PortfolioPage /></ProtectedRoute> 
  },
  {
    path: "/news", // Add the NewsPage route
    element: <NewsPage />,
  },
  {
    path: "/aboutus", // Add the NewsPage route
    element: <AboutUs />,
  },
  {
    path: "/settings", // Add the NewsPage route
    element: <UserSettings />,
  }
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
