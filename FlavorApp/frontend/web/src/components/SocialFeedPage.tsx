
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const SocialFeedPage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>SocialFeedPage works!</div>
        </ThemeProvider>
    );
};

export default SocialFeedPage;
