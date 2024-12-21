import {useContext} from 'react';
import {ThemeContext} from './ThemeContext';

const useTheme = () => {
    const context = useContext(ThemeContext);

    if(!context){
        throw new Error('ThemeContext is not provided')
    }

    return context;
}

export default useTheme;