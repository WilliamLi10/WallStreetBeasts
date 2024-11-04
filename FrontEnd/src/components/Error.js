import { useNavigate, useLocation } from "react-router-dom";
import { BiErrorAlt } from "react-icons/bi";

const Error = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="flex flex-col px-5 pt-16 items-center">
      <div className="flex flex-row items-center">
        <BiErrorAlt className="h-16 w-16 text-red-600 mr-2" />
        <div className="flex flex-col">
          <p className="text-2xl font-bold">
            {location.state ? location.state.status : "404"} Error
          </p>
          <p>
            {location.state ? location.state.error : "Page not found"}
          </p>
        </div>
      </div>
      <button
        className="border-solid border-[1px] border-slate-700 font-thin rounded-full px-4 py-2 mt-5 transition-all duration-150 hover:text-white hover:bg-slate-700"
        onClick={() => {
          navigate("/");
        }}
      >
        Go Back
      </button>
    </div>
  );
};

export default Error;
