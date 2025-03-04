
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';

const MealPlanPage: React.FC = () => {
    const darkTheme = createTheme({
        palette: {
            mode: 'dark',
        },
    });

    return (
        <ThemeProvider theme={darkTheme}>
            <div>MealPlanPage works!</div>
        </ThemeProvider>
    );
};

export default MealPlanPage;
