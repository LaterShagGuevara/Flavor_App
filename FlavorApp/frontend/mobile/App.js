
import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider } from 'react-redux';
import store from './src/redux/store';
import { ThemeProvider } from 'styled-components/native';

const Stack = createStackNavigator();

export default function App() {
  const [darkMode, setDarkMode] = useState(true);

  const theme = {
    mode: darkMode ? 'dark' : 'light',
    colors: darkMode ? {
      background: '#121212',
      text: '#ffffff',
      primary: '#bb86fc',
    } : {
      background: '#ffffff',
      text: '#000000',
      primary: '#6200ee',
    }
  };

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <NavigationContainer>
          <Stack.Navigator>
            {/* Mobile App Routes */}
          </Stack.Navigator>
        </NavigationContainer>
      </ThemeProvider>
    </Provider>
  );
}
