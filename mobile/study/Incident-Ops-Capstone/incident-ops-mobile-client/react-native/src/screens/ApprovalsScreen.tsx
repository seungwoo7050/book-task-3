import React from 'react';
import { FlatList, StyleSheet, Text } from 'react-native';

import { usePendingApprovalItems } from '../app/AppModel';
import { EmptyState, MetricRow, ScreenLayout, SectionCard, StatusPill } from '../components/Ui';
import { theme } from '../theme';

export function ApprovalsScreen() {
  const { items } = usePendingApprovalItems();

  return (
    <ScreenLayout scroll={false} contentStyle={styles.screenBody}>
      <FlatList
        contentContainerStyle={styles.listContent}
        data={items}
        keyExtractor={item => item.id}
        ListEmptyComponent={
          <EmptyState
            body="이 탭은 `RESOLUTION_PENDING` incident를 별도로 모아서 approver 시나리오를 빠르게 검토하게 해 줍니다."
            title="No pending approvals"
          />
        }
        ListHeaderComponent={
          <SectionCard eyebrow="Approver View" title="Pending Decisions">
            <Text style={styles.lead}>
              별도 approvals endpoint 없이 incident feed와 approvalId를 이용해 승인 대기열을 구성합니다.
            </Text>
          </SectionCard>
        }
        renderItem={({ item }) => (
          <SectionCard eyebrow={item.severity} title={item.title}>
            <StatusPill label={item.status} />
            <MetricRow label="Approval ID" value={item.approvalId ?? 'missing'} />
            <MetricRow label="Sync" value={item.syncState} />
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
  lead: {
    color: theme.color.mutedInk,
    fontSize: 15,
    lineHeight: 22,
  },
});
