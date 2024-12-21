import React from 'react';
import useTheme from '../context/ThemeContext/useTheme'

const ThemeToggle: React.FC = () => {
    const {theme , toggleTheme} = useTheme();
    return (
        <button onClick={toggleTheme} className=" button theme-toggle-btn">
            Toggle Theme: {theme==='light' ? 'Dark' : 'Light '}
        </button>
    )
}

export default ThemeToggle;