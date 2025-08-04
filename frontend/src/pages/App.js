import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from '@react-oauth/google';

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleClassicLogin = async (e) => {
    e.preventDefault();
    
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    } else {
      alert("Invalid credentials");
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    const idToken = credentialResponse.credential;
    // Envoi au backend pour vérification
    const response = await fetch("http://localhost:8000/auth/google", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_token: idToken })
    });
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    } else {
      alert("Google login failed");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Welcome to Jarvis</h2>

        {/* Login Form */}
        <form onSubmit={handleClassicLogin} className="space-y-4">
          <div>
            <label className="block text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter your username"
              required
            />
          </div>
          <div>
            <label className="block text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter your password"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition duration-200"
          >
            Login
          </button>
        </form>

        <div className="my-6 text-center text-gray-500">OR</div>

        {/* Google Login */}
        <div className="flex justify-center">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => alert("Google Sign-In failed")}
          />
        </div>
      </div>
    </div>
  );
}
