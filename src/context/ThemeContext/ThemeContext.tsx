import React, { createContext, useState, ReactNode } from 'react';
import { Theme, ThemeContextType } from './ThemeTypes';

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)


interface ThemeProviderProps{
    children: ReactNode
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({children}) => {
    const [theme, setTheme] = useState<Theme>('light') // default themes
    const toggleTheme = () => {
        setTheme(theme === 'light' ? 'dark' : 'light')
    }

    return (
        <ThemeContext.Provider value={{theme, toggleTheme}}>
            {children}
        </ThemeContext.Provider>
    )

}

export default ThemeContext;