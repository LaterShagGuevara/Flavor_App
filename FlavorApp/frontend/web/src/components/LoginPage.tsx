
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const LoginPage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>LoginPage works!</div>
        </ThemeProvider>
    );
};

export default LoginPage;
