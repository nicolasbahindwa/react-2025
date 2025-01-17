
// import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom';
import { routes } from './config/routes';
import MainLayout from './layouts/(MainLayout)';
import AuthLayout from './layouts/(AuthLayout)';
import DashboardLayout from './layouts/(DashboardLayout)';
import HomePage from './pages/public/HomePage';
import LoginPage from './features/Auth/LoginPage';
import RegisterPage from './features/Auth/RegisterPage';
import ChatInterface from './features/ChatEngine/chat';
import DashboardPage from './pages/private/DashboardPage';
import UserProfilePage from './pages/private/UserProfilePage';
import ThemeProviderWrapper from "./context/ThemeContext/ThemeProvider";

import { Provider } from 'react-redux';
import {PersistGate} from 'redux-persist/integration/react';
import {store, persistor} from '@/store';

 
 

function App() {
 

  return (
    
    <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <ThemeProviderWrapper>
           
          <Routes>
            {/* Public Routes */}
            <Route path={routes.home} element={<MainLayout />}>
                <Route index element={<HomePage />} />
            </Route>
            <Route path={routes.chat} element={<MainLayout />}>
                <Route index element={<ChatInterface />} />
            </Route>
            <Route path={routes.login} element={<AuthLayout />}>
              <Route index element={<LoginPage />} />
            </Route>

            <Route path={routes.register} element={<AuthLayout />}>
              <Route index element={<RegisterPage />} />
            </Route>
            


            {/* Private Routes */}
            <Route path={routes.dashboard} element={<DashboardLayout />}>
              <Route index element={<DashboardPage />} />
              <Route path={routes.profile} element={<UserProfilePage />} />
            </Route>

            {/* Redirect Unknown Routes */}
            <Route path="*" element={<Navigate to={routes.home} />} />
          </Routes>
      
         
        </ThemeProviderWrapper>
      </PersistGate>
    </Provider>
    
  );
}

export default App
