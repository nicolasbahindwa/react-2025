import React from 'react';
import useTheme from '../context/ThemeContext/useTheme'
import { Moon, Sun } from 'lucide-react';

const ThemeToggle: React.FC = () => {
    const {theme , toggleTheme} = useTheme();
    return (
        <button onClick={toggleTheme} className="btn ">
            {theme === 'light' ? <Moon  className='icon-xs'/> : <Sun className='icon-xs'/>} 
        </button>
    )
}

export default ThemeToggle;