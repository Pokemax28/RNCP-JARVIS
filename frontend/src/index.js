import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './pages/App';
import MainDashboard from './pages/MainDashboard';
import Register from './pages/Register';
import './index.css';
import EmailDashboard from './pages/EmailDashboard';

const clientId = '874723136470-nrmckle5mk1q2qrc2ppmg3d593co3e91.apps.googleusercontent.com';

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/" />;
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={clientId}>
      <Router>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<PrivateRoute><MainDashboard /></PrivateRoute>} />
          <Route path="/emails" element={<PrivateRoute><EmailDashboard /></PrivateRoute>} />
        </Routes>
      </Router>
    </GoogleOAuthProvider>
  </React.StrictMode>
);
