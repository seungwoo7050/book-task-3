import React from 'react';
import {
  NavigationContainer,
  type InitialState,
} from '@react-navigation/native';
import { StatusBar } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { linking } from './src/navigation/linking';
import { RootNavigator } from './src/navigation/RootNavigator';
import { navigationTheme, palette } from './src/theme';

type AppProps = {
  initialState?: InitialState;
};

function App({ initialState }: AppProps) {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <StatusBar
          backgroundColor={palette.midnight}
          barStyle="light-content"
        />
        <NavigationContainer
          initialState={initialState}
          linking={linking}
          theme={navigationTheme}
        >
          <RootNavigator />
        </NavigationContainer>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

export default App;
