import React, { createContext, useState, ReactNode, useEffect } from 'react';
import { Theme, ThemeContextType } from './ThemeTypes';

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Get the theme from localStorage, if it exists
  const savedTheme = localStorage.getItem('theme') as Theme | null;

  // Fallback to 'light' if the saved theme is invalid or not present
  const initialTheme = savedTheme === 'dark' || savedTheme === 'light' ? savedTheme : 'light';

  // Set the initial theme
  const [theme, setTheme] = useState<Theme>(initialTheme);

  // Toggle the theme between light and dark
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme); // Save the new theme to localStorage
  };

  useEffect(() => {
    document.body.setAttribute('data-theme', theme); // Apply the theme to the body element
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeContext;
