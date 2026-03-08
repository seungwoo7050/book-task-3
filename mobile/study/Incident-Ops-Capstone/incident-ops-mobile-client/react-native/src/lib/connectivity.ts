import NetInfo, { type NetInfoState } from '@react-native-community/netinfo';

import type { ConnectionState } from './types';

export function toConnectionState(state: NetInfoState): ConnectionState {
  return {
    isConnected: Boolean(
      state.isConnected && state.isInternetReachable !== false,
    ),
    typeLabel: state.type ?? 'unknown',
    updatedAt: new Date().toISOString(),
  };
}

export async function fetchCurrentConnection(): Promise<ConnectionState> {
  const state = await NetInfo.fetch();
  return toConnectionState(state);
}

export function subscribeToConnectivity(
  listener: (state: ConnectionState) => void,
): () => void {
  return NetInfo.addEventListener(state => {
    listener(toConnectionState(state));
  });
}
