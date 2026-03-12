import { jest } from '@jest/globals';

Object.defineProperty(global, 'fetch', {
  configurable: true,
  value: jest.fn(),
});
