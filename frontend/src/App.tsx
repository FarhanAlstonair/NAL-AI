import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './layouts/Navbar';
import Footer from './layouts/Footer';
import HomePage from './pages/Home';
import LoginPage from './pages/Auth/Login';

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/register" element={<div>Register Page</div>} />
          <Route path="/properties" element={<div>Properties Page</div>} />
          <Route path="/properties/:id" element={<div>Property Detail Page</div>} />
          <Route path="/dashboard" element={<div>Dashboard</div>} />
          <Route path="*" element={<div>404 Not Found</div>} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;