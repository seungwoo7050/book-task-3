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

Object.defineProperty(global, 'fetch', {
  configurable: true,
  value: jest.fn(),
});

class MockWebSocket {
  static OPEN = 1;

  url: string;
  readyState = MockWebSocket.OPEN;
  onopen: (() => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: (() => void) | null = null;
  onmessage: ((event: { data: string }) => void) | null = null;

  constructor(url: string) {
    this.url = url;
    queueMicrotask(() => {
      this.onopen?.();
    });
  }

  send(_payload: string): void {}

  close(): void {
    this.onclose?.();
  }
}

Object.defineProperty(global, 'WebSocket', {
  configurable: true,
  value: MockWebSocket,
});

jest.mock('react-native-gesture-handler', () => {
  const React = require('react');
  const { View } = require('react-native');

  return {
    GestureHandlerRootView: ({ children }: { children: React.ReactNode }) =>
      React.createElement(View, null, children),
    Directions: {},
    State: {},
  };
});

jest.mock('react-native-reanimated', () => {
  const { View } = require('react-native');

  return {
    __esModule: true,
    default: {
      call: () => {},
      createAnimatedComponent: (Component: unknown) => Component,
    },
    View,
    useSharedValue: <T>(value: T) => ({ value }),
    useAnimatedStyle: () => ({}),
    useDerivedValue: <T>(factory: () => T) => ({ value: factory() }),
    withTiming: <T>(value: T) => value,
    withSpring: <T>(value: T) => value,
    runOnJS: <T extends (...args: never[]) => unknown>(fn: T) => fn,
    runOnUI: <T extends (...args: never[]) => unknown>(fn: T) => fn,
    cancelAnimation: () => {},
    Easing: {},
  };
}, { virtual: true });

jest.mock('react-native-safe-area-context', () => {
  const React = require('react');
  const { View } = require('react-native');
  const insets = {
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
  };
  const frame = {
    x: 0,
    y: 0,
    width: 320,
    height: 640,
  };
  const SafeAreaInsetsContext = React.createContext(insets);
  const SafeAreaFrameContext = React.createContext(frame);

  return {
    __esModule: true,
    SafeAreaInsetsContext,
    SafeAreaFrameContext,
    SafeAreaProvider: ({ children }: { children: React.ReactNode }) =>
      React.createElement(
        SafeAreaFrameContext.Provider,
        { value: frame },
        React.createElement(
          SafeAreaInsetsContext.Provider,
          { value: insets },
          React.createElement(View, null, children),
        ),
      ),
    SafeAreaView: ({
      children,
      style,
    }: {
      children: React.ReactNode;
      style?: unknown;
    }) => React.createElement(View, { style }, children),
    initialWindowMetrics: {
      insets,
      frame,
    },
    useSafeAreaInsets: () => insets,
    useSafeAreaFrame: () => frame,
  };
});

jest.mock('@react-native-async-storage/async-storage', () => {
  const store = new Map<string, string>();

  return {
    __esModule: true,
    default: {
      async getItem(key: string) {
        return store.get(key) ?? null;
      },
      async setItem(key: string, value: string) {
        store.set(key, value);
      },
      async removeItem(key: string) {
        store.delete(key);
      },
      async clear() {
        store.clear();
      },
    },
  };
});

jest.mock('@react-native-community/netinfo', () => {
  return {
    __esModule: true,
    default: {
      addEventListener: (listener: (state: object) => void) => {
        listener({
          isConnected: true,
          isInternetReachable: true,
          type: 'wifi',
        });
        return () => {};
      },
      fetch: () =>
        Promise.resolve({
          isConnected: true,
          isInternetReachable: true,
          type: 'wifi',
        }),
    },
  };
});
