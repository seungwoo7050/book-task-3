module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?|@react-navigation|@incident-ops/contracts|react-native-drawer-layout|react-native-gesture-handler|react-native-safe-area-context|react-native-screens)/)',
  ],
};
