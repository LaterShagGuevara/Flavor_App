
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const ProfilePage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>ProfilePage works!</div>
        </ThemeProvider>
    );
};

export default ProfilePage;
