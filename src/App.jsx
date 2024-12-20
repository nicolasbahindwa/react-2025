import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom';
import { routes } from './config/routes';
import MainLayout from './layouts/(MainLayout)';
import AuthLayout from './layouts/(AuthLayout)';
import DashboardLayout from './layouts/(DashboardLayout)';
import HomePage from './pages/public/HomePage';
import LoginPage from './pages/public/LoginPage';
import DashboardPage from './pages/private/DashboardPage';
import UserProfilePage from './pages/private/UserProfilePage';

 

function App() {
 

  return (
     <Routes>
        {/* Public Routes */}
        <Route app={routes.home} element= {<MainLayout/>}>
            <Route index element={<HomePage/>}/>
        </Route>
        <Route path={routes.login} element={<AuthLayout />}>
          <Route index element={<LoginPage />} />
        </Route>
      
        {/* Private Routes */}
        <Route path={routes.dashboard} element={<DashboardLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path={routes.profile} element={<UserProfilePage />} />
        </Route>

        {/* Redirect Unknown Routes */}
        <Route path="*" element={<Navigate to={routes.home} />} />

     </Routes>
  )
}

export default App
