import React from 'react';
import { ActivityIndicator, FlatList, StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

import { useAppModel, useIncidentItems } from '../app/AppModel';
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
import type { IncidentStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<IncidentStackParamList, 'IncidentFeed'>;

function incidentOpenTestId(title: string): string {
  return `incident-open-${title
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')}`;
}

function statusTone(status: string): 'neutral' | 'info' | 'success' | 'warning' {
  switch (status) {
    case 'OPEN':
      return 'warning';
    case 'ACKED':
      return 'info';
    case 'RESOLUTION_PENDING':
      return 'neutral';
    default:
      return 'success';
  }
}

export function IncidentsScreen({ navigation }: Props) {
  const { connection, outbox, streamStatus } = useAppModel();
  const {
    items,
    isLoading,
    isFetching,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useIncidentItems();
  const outboxSummary = summarizeOutbox(outbox);

  return (
    <ScreenLayout scroll={false} contentStyle={styles.screenBody}>
      <FlatList
        contentContainerStyle={styles.listContent}
        data={items}
        keyExtractor={item => item.id}
        ListEmptyComponent={
          isLoading ? (
            <ActivityIndicator color={theme.color.accent} size="large" />
          ) : (
            <EmptyState
              body="로그인 직후 incident feed가 비어 있으면 reporter로 새 incident를 생성해 흐름을 시작하세요."
              title="No incidents yet"
            />
          )
        }
        ListFooterComponent={
          hasNextPage ? (
            <ActionButton
              disabled={isFetchingNextPage}
              label={isFetchingNextPage ? 'Loading...' : 'Load more'}
              onPress={() => {
                void fetchNextPage();
              }}
            />
          ) : null
        }
        ListHeaderComponent={
          <View style={sharedStyles.gapMd}>
            <SectionCard eyebrow="Main Tabs" title="Operational Feed">
              <MetricRow
                label="Connection"
                value={`${connection.isConnected ? 'online' : 'offline'} / ${connection.typeLabel}`}
              />
              <MetricRow label="Stream" value={streamStatus} />
              <MetricRow
                label="Outbox"
                value={`pending ${outboxSummary.pending}, failed ${outboxSummary.failed}`}
              />
              <View style={sharedStyles.row}>
                <ActionButton
                  label="New Incident"
                  onPress={() => navigation.navigate('CreateIncident')}
                  testID="new-incident-button"
                />
                <ActionButton
                  disabled={isFetching}
                  label={isFetching ? 'Refreshing...' : 'Refresh'}
                  onPress={() => {
                    void refetch();
                  }}
                  tone="ghost"
                />
              </View>
            </SectionCard>
          </View>
        }
        renderItem={({ item }) => (
          <SectionCard eyebrow={item.severity} title={item.title}>
            <View style={sharedStyles.rowWrap}>
              <StatusPill label={item.status} tone={statusTone(item.status)} />
              <StatusPill
                label={item.syncState === 'live' ? 'live' : item.syncState}
                tone={item.syncState === 'failed' ? 'danger' : 'info'}
              />
            </View>
            <Text style={styles.description} numberOfLines={2}>
              {item.description || 'No description'}
            </Text>
            <MetricRow label="Created By" value={item.createdBy} />
            <MetricRow label="Updated" value={item.updatedAt} />
            {item.pendingActions.length ? (
              <Text style={styles.pendingText}>
                pending actions: {item.pendingActions.join(', ')}
              </Text>
            ) : null}
            <ActionButton
              label="Open"
              onPress={() =>
                navigation.navigate('IncidentDetail', { incidentId: item.id })
              }
              testID={incidentOpenTestId(item.title)}
            />
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
  description: {
    color: theme.color.mutedInk,
    fontSize: 15,
    lineHeight: 22,
  },
  pendingText: {
    color: theme.color.info,
    fontSize: 13,
    fontWeight: '600',
  },
});
