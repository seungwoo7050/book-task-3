import React from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';

import { useAppModel } from '../app/AppModel';
import {
  ActionButton,
  EmptyState,
  MetricRow,
  ScreenLayout,
  SectionCard,
  StatusPill,
  sharedStyles,
} from '../components/Ui';
import { summarizeOutbox } from '../lib/outbox';
import { theme } from '../theme';

export function OutboxScreen() {
  const {
    outbox,
    retryFailedMutation,
    clearSyncedMutations,
    flushPendingMutations,
  } = useAppModel();
  const summary = summarizeOutbox(outbox);

  return (
    <ScreenLayout scroll={false} contentStyle={styles.screenBody}>
      <FlatList
        contentContainerStyle={styles.listContent}
        data={outbox}
        keyExtractor={item => item.id}
        ListEmptyComponent={
          <EmptyState
            body="mutation이 큐에 들어오면 여기에서 pending, synced, failed 상태와 retry 횟수를 확인할 수 있습니다."
            title="Outbox is empty"
          />
        }
        ListHeaderComponent={
          <SectionCard eyebrow="Offline First" title="Persistent Outbox">
            <MetricRow label="Pending" value={String(summary.pending)} />
            <MetricRow label="Synced" value={String(summary.synced)} />
            <MetricRow label="Failed" value={String(summary.failed)} />
            <View style={sharedStyles.row}>
              <ActionButton
                label="Flush Pending"
                onPress={() => {
                  void flushPendingMutations();
                }}
                testID="outbox-flush-button"
              />
              <ActionButton
                label="Clear Synced"
                onPress={clearSyncedMutations}
                testID="outbox-clear-synced-button"
                tone="ghost"
              />
            </View>
          </SectionCard>
        }
        renderItem={({ item }) => (
          <SectionCard eyebrow={item.action} title={item.label}>
            <View style={sharedStyles.rowWrap}>
              <StatusPill
                label={item.state}
                tone={item.state === 'failed' ? 'danger' : 'info'}
              />
              <StatusPill label={`attempts ${item.attempts}`} tone="neutral" />
            </View>
            <Text style={styles.meta}>created at {item.createdAt}</Text>
            {item.lastError ? <Text style={styles.error}>{item.lastError}</Text> : null}
            {item.state === 'failed' ? (
              <ActionButton
                label="Retry Failed Job"
                onPress={() => retryFailedMutation(item.id)}
                testID="outbox-retry-failed-button"
              />
            ) : null}
          </SectionCard>
        )}
      />
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  screenBody: {
    paddingHorizontal: 0,
    paddingVertical: 0,
  },
  listContent: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  meta: {
    color: theme.color.mutedInk,
    fontSize: 13,
  },
  error: {
    color: theme.color.danger,
    fontSize: 14,
  },
});
