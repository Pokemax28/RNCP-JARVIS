import { useNavigate } from "react-router-dom";
import { Calendar } from "../components/ui/calendar"; // 👈 Import ici

export default function MainDashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-indigo-600 text-white flex justify-between items-center p-4">
        <h1 className="text-2xl font-bold">Jarvis Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-white text-indigo-600 font-semibold px-4 py-2 rounded hover:bg-gray-100"
        >
          Logout
        </button>
      </header>

      {/* Calendar intégré */}
      <div className="p-4">
        <div className="bg-white rounded shadow p-6">
          <Calendar /> {/* 👈 Ton composant réel */}
        </div>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
        <div
          className="bg-white rounded shadow p-6 flex items-center justify-center text-3xl cursor-pointer hover:bg-gray-50"
          onClick={() => navigate("/emails")}
        >
          📧
        </div>
        <div className="bg-white rounded shadow p-6 flex items-center justify-center text-xl text-gray-500">
          In Progress
        </div>
        <div className="bg-white rounded shadow p-6 flex items-center justify-center text-xl text-gray-500">
          In Progress
        </div>
        <div className="bg-white rounded shadow p-6 flex items-center justify-center text-xl text-gray-500">
          In Progress
        </div>
      </div>
    </div>
  );
}
