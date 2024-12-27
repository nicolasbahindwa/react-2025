import React, {useEffect}from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../../components/shared/layout/Header';
import Footer from '../../components/shared/layout/Footer';

import  ThemeProviderWrapper  from "../../context/ThemeContext/ThemeProvider";
import useTheme from "../../context/ThemeContext/useTheme";

// Import global and theme-specific CSS
// import "../../assets/styles/global.css";
// import "../../assets/styles/themes/light.css";
// import "../../assets/styles/themes/dark.css";
// import "../../assets/styles/themes/ThemeToggle.css"
import "../../assets/styles/main.scss"

const MainLayout: React.FC = () => {
    const {theme}  = useTheme();

    // Dynamically set the theme
    useEffect(() => {
      document.body.setAttribute("data-theme", theme);
    }, [theme]);

    return (
        
        <>
       
            <Header />
            <main>
                <Outlet />
            </main>
            <Footer />
         
        </>
    );
};

export default MainLayout;
