// src/context/ThemeContext/ThemeProviderWrapper.tsx

import React, { ReactNode } from "react";
import { ThemeProvider as CustomThemeProvider } from "./ThemeContext";

interface ThemeProviderWrapperProps {
  children: ReactNode;
}

const ThemeProviderWrapper: React.FC<ThemeProviderWrapperProps> = ({
  children,
}) => {
  return (
    <CustomThemeProvider>
        {children}
    </CustomThemeProvider>
  )
};

export default ThemeProviderWrapper;
