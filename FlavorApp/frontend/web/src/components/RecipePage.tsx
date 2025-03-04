
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const RecipePage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>RecipePage works!</div>
        </ThemeProvider>
    );
};

export default RecipePage;
