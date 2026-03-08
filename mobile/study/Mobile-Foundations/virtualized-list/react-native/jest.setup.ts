import { jest } from '@jest/globals';

jest.mock('@shopify/flash-list', () => {
  const React = require('react');
  const { FlatList } = require('react-native');

  return {
    FlashList: ({ children, ...props }: Record<string, unknown>) =>
      React.createElement(FlatList, props, children),
  };
});
