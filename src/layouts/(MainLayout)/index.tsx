import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../../components/shared/layout/Header';
import Footer from '../../components/shared/layout/Footer';

const MainLayout: React.FC = () => {
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
