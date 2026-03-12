import 'react-native-gesture-handler/jestSetup';
import { jest } from '@jest/globals';

const workletsProxy = new Proxy(
  {
    createSerializableBoolean: (value: boolean) => value,
    createSerializableNull: () => null,
    createSerializableUndefined: () => undefined,
    createSerializableArray: (value: unknown[]) => value,
    createSerializableFunction: <T>(value: T) => value,
    createSerializableHostObject: <T>(value: T) => value,
    createSerializableImport: () => ({}),
    createSerializableInitializer: <T>(value: T) => value,
    createSerializableMap: (
      keys: Array<string | number | symbol>,
      values: unknown[],
    ) => new Map(keys.map((key, index) => [key, values[index]])),
    createSerializableNumber: (value: number) => value,
    createSerializableObject: <T>(value: T) => value,
    createSerializableSet: (values: unknown[]) => new Set(values),
    createSerializableString: (value: string) => value,
    createSerializableTurboModuleLike: <T>(value: T) => value,
    createSerializableWorklet: <T>(value: T) => value,
    createSynchronizable: <T>(value: T) => value,
    executeOnUIRuntimeSync: <T>(value: T) => value,
    registerCustomSerializable: () => undefined,
    reportFatalErrorOnJS: () => undefined,
    scheduleOnRuntime: () => undefined,
    scheduleOnUI: () => undefined,
    synchronizableGetBlocking: <T>(value: T) => value,
    synchronizableGetDirty: <T>(value: T) => value,
    synchronizableLock: () => undefined,
    synchronizableSetBlocking: () => undefined,
    synchronizableUnlock: () => undefined,
  },
  {
    get(target, property) {
      if (property in target) {
        return target[property as keyof typeof target];
      }

      return () => undefined;
    },
  },
);

Object.defineProperty(global, '__workletsModuleProxy', {
  configurable: true,
  value: workletsProxy,
});

jest.mock('react-native-gesture-handler', () => {
  const React = require('react');
  const actual = jest.requireActual(
    'react-native-gesture-handler',
  ) as Record<string, unknown>;
  const { View } = require('react-native');

  return {
    ...actual,
    GestureHandlerRootView: ({ children }: { children: React.ReactNode }) =>
      React.createElement(View, null, children),
  };
});

jest.mock('react-native-reanimated', () => {
  const Reanimated = require('react-native-reanimated/mock');

  Reanimated.default.call = () => {};
  return Reanimated;
});
jest.mock('react-native-safe-area-context', () =>
  require('react-native-safe-area-context/jest/mock'),
);
