import { DefaultTheme } from '@react-navigation/native';

export const palette = {
  midnight: '#112034',
  slate: '#203754',
  mist: '#eaf1f7',
  coral: '#ff845e',
  gold: '#f4c95d',
  teal: '#38b2ac',
  ink: '#213047',
  panel: '#f7fbff',
  border: '#c8d7e6',
  shadow: '#13253d',
};

export const navigationTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: palette.coral,
    background: palette.panel,
    card: '#ffffff',
    text: palette.ink,
    border: palette.border,
    notification: palette.gold,
  },
};
