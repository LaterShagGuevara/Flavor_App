
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const HomePage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>HomePage works!</div>
        </ThemeProvider>
    );
};

export default HomePage;
