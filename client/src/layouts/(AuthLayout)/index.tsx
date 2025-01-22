import React, {useEffect}from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../../components/shared/layout/Header';
import Footer from '../../components/shared/layout/Footer';
import useTheme from "../../context/ThemeContext/useTheme";
 
 

function Login() {
  const {theme}  = useTheme();
  useEffect(() => {
     
    document.body.setAttribute("data-theme", theme);
  }, [theme])
  return (
    <>
      <Header />
      <main className="w-full" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default Login