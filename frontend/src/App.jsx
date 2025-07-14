// frontend/src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Importe os componentes de página que vamos criar
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
// Futuramente: import DashboardPage from './pages/DashboardPage';
// Futuramente: import ProfilePage from './pages/ProfilePage';
// Futuramente: import RegistroProgressoPage from './pages/RegistroProgressoPage';

function App() {
  // Aqui, futuramente, teremos a lógica de autenticação do usuário
  // Por enquanto, vamos considerar que o usuário não está autenticado por padrão
  const isAuthenticated = false; // Isso será dinâmico depois com o Context API

  return (
    <Router>
      <div className="App">
        {/* Você pode adicionar um Navbar aqui depois */}
        <Routes>
          {/* Rota para a página de Login */}
          <Route path="/login" element={<LoginPage />} />

          {/* Rota para a página de Registro */}
          <Route path="/register" element={<RegisterPage />} />

          {/* Rota para a página inicial, redireciona para login se não autenticado */}
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <div>Bem-vindo! Esta é a página inicial. (Futuro Dashboard)</div>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Exemplo de rota protegida (futuramente) */}
          {/*
          <Route
            path="/dashboard"
            element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/profile"
            element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/registros"
            element={isAuthenticated ? <RegistroProgressoPage /> : <Navigate to="/login" replace />}
          />
          */}

          {/* Rota para lidar com caminhos não encontrados (404) - opcional */}
          <Route path="*" element={<h2>404 - Página Não Encontrada</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;