// App.js
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import StockDisplayPage from "./pages/StockDisplayPage";
import Error from "./components/Error";
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
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
