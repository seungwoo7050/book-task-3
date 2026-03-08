import React, { useEffect, useState } from 'react';
import { StyleSheet, Text } from 'react-native';

import { useAppModel } from '../app/AppModel';
import {
  ActionButton,
  AppTextField,
  MetricRow,
  ScreenLayout,
  SectionCard,
} from '../components/Ui';
import { theme } from '../theme';

export function SettingsScreen() {
  const {
    connection,
    flushPendingMutations,
    lastEventId,
    logout,
    session,
    settings,
    streamStatus,
    updateBaseUrl,
  } = useAppModel();
  const [baseUrl, setBaseUrl] = useState(settings.baseUrl);
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    setBaseUrl(settings.baseUrl);
  }, [settings.baseUrl]);

  async function saveNextBaseUrl(): Promise<void> {
    setSaveError(null);
    try {
      await updateBaseUrl(baseUrl);
    } catch (error) {
      setSaveError(error instanceof Error ? error.message : 'save failed');
    }
  }

  return (
    <ScreenLayout scroll>
      <SectionCard eyebrow="Runtime" title="Connection And Session">
        <MetricRow label="Actor" value={session?.actor.userId ?? 'signed out'} />
        <MetricRow label="Role" value={session?.actor.role ?? 'none'} />
        <MetricRow
          label="Connection"
          value={`${connection.isConnected ? 'online' : 'offline'} / ${connection.typeLabel}`}
        />
        <MetricRow label="Stream" value={streamStatus} />
        <MetricRow label="Last Event ID" value={String(lastEventId)} />
      </SectionCard>

      <SectionCard title="Backend Target">
        <AppTextField
          autoCapitalize="none"
          label="Base URL"
          onChangeText={setBaseUrl}
          placeholder="http://127.0.0.1:4100"
          testID="settings-base-url-input"
          value={baseUrl}
        />
        {saveError ? <Text style={styles.error}>{saveError}</Text> : null}
        <ActionButton
          label="Save Base URL"
          onPress={() => void saveNextBaseUrl()}
          testID="settings-save-base-url-button"
        />
      </SectionCard>

      <SectionCard title="Maintenance">
        <ActionButton
          label="Flush Pending Mutations"
          onPress={() => {
            void flushPendingMutations();
          }}
          testID="settings-flush-button"
        />
        <ActionButton
          label="Sign Out And Reset Session"
          onPress={() => {
            void logout();
          }}
          testID="settings-signout-button"
          tone="danger"
        />
      </SectionCard>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  error: {
    color: theme.color.danger,
    fontSize: 14,
  },
});
