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
    <div className='container-flex'>
      <Header />
      <main className="w-full">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default Login