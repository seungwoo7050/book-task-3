import React, { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

import { useAppModel, useIncidentAudit, useIncidentItems } from '../app/AppModel';
import {
  ActionButton,
  AppTextField,
  EmptyState,
  MetricRow,
  ScreenLayout,
  SectionCard,
  StatusPill,
  sharedStyles,
} from '../components/Ui';
import { approvalDecisionSchema, resolutionSchema } from '../lib/forms';
import { theme } from '../theme';
import type { IncidentStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<IncidentStackParamList, 'IncidentDetail'>;

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

export function IncidentDetailScreen({ route }: Props) {
  const { incidentId } = route.params;
  const {
    outbox,
    queueAckIncident,
    queueApprovalDecision,
    queueRequestResolution,
    session,
  } = useAppModel();
  const { items } = useIncidentItems();
  const auditQuery = useIncidentAudit(incidentId);
  const [note, setNote] = useState('');
  const [actionError, setActionError] = useState<string | null>(null);

  const incident = items.find(item => item.id === incidentId);
  const relatedJobs = outbox.filter(item =>
    item.action === 'POST /incidents'
      ? `local-${item.id}` === incidentId
      : item.payload.incidentId === incidentId,
  );

  if (!incident) {
    return (
      <ScreenLayout scroll>
        <EmptyState
          body="incident feed에서 선택한 항목을 찾지 못했습니다. feed를 새로고침한 뒤 다시 열어 보세요."
          title="Incident not found"
        />
      </ScreenLayout>
    );
  }

  const currentIncident = incident;

  const canAck =
    session?.actor.role === 'OPERATOR' &&
    currentIncident.status === 'OPEN' &&
    currentIncident.source === 'server';
  const canRequestResolution =
    session?.actor.role === 'OPERATOR' &&
    currentIncident.status === 'ACKED' &&
    currentIncident.source === 'server';
  const canDecide =
    session?.actor.role === 'APPROVER' &&
    currentIncident.status === 'RESOLUTION_PENDING' &&
    currentIncident.approvalId !== null &&
    currentIncident.source === 'server';

  function submitRequestResolution(): void {
    setActionError(null);
    const parsed = resolutionSchema.safeParse({ reason: note });
    if (!parsed.success) {
      setActionError(parsed.error.issues[0]?.message ?? 'invalid reason');
      return;
    }

    queueRequestResolution(currentIncident.id, { reason: parsed.data.reason });
    setNote('');
  }

  function submitDecision(decision: 'APPROVE' | 'REJECT'): void {
    setActionError(null);
    const parsed = approvalDecisionSchema.safeParse({ decision, note });
    if (!parsed.success) {
      setActionError(parsed.error.issues[0]?.message ?? 'invalid note');
      return;
    }

    if (!currentIncident.approvalId) {
      setActionError('approval id is missing');
      return;
    }

    queueApprovalDecision({
      incidentId: currentIncident.id,
      approvalId: currentIncident.approvalId,
      decision,
      note: parsed.data.note,
    });
    setNote('');
  }

  return (
    <ScreenLayout scroll>
      <SectionCard eyebrow={currentIncident.severity} title={currentIncident.title}>
        <View style={sharedStyles.rowWrap}>
          <StatusPill
            label={currentIncident.status}
            tone={statusTone(currentIncident.status)}
          />
          <StatusPill
            label={
              currentIncident.syncState === 'live'
                ? 'live'
                : currentIncident.syncState
            }
            tone={currentIncident.syncState === 'failed' ? 'danger' : 'info'}
          />
        </View>
        <Text style={styles.description}>
          {currentIncident.description || 'No description'}
        </Text>
        <MetricRow label="Created By" value={currentIncident.createdBy} />
        <MetricRow
          label="Approval ID"
          value={currentIncident.approvalId ?? 'none'}
        />
        <MetricRow label="Updated" value={currentIncident.updatedAt} />
      </SectionCard>

      <SectionCard title="Role Actions">
        {canAck ? (
          <ActionButton
            label="Queue Ack"
            onPress={() => {
              queueAckIncident(incident.id);
            }}
            testID="detail-ack-button"
          />
        ) : null}

        {(canRequestResolution || canDecide) ? (
          <AppTextField
            label={canRequestResolution ? 'Resolution Reason' : 'Decision Note'}
            multiline
            onChangeText={setNote}
            placeholder={
              canRequestResolution
                ? 'Mitigation is complete and evidence is attached.'
                : 'Optional review note for the approval decision'
            }
            testID="detail-action-note-input"
            value={note}
          />
        ) : null}

        {canRequestResolution ? (
          <ActionButton
            label="Queue Request Resolution"
            onPress={submitRequestResolution}
            testID="detail-request-resolution-button"
          />
        ) : null}

        {canDecide ? (
          <View style={sharedStyles.row}>
            <ActionButton
              label="Approve"
              onPress={() => submitDecision('APPROVE')}
              testID="detail-approve-button"
            />
            <ActionButton
              label="Reject"
              onPress={() => submitDecision('REJECT')}
              testID="detail-reject-button"
              tone="danger"
            />
          </View>
        ) : null}

        {!canAck && !canRequestResolution && !canDecide ? (
          <Text style={styles.caption}>
            현재 역할과 incident 상태에서는 추가 action이 없습니다.
          </Text>
        ) : null}

        {actionError ? <Text style={styles.error}>{actionError}</Text> : null}
      </SectionCard>

      <SectionCard title="Outbox Overlay">
        {relatedJobs.length ? (
          relatedJobs.map(job => (
            <View key={job.id} style={styles.jobRow}>
              <Text style={styles.jobLabel}>{job.label}</Text>
              <StatusPill
                label={job.state}
                tone={job.state === 'failed' ? 'danger' : 'info'}
              />
            </View>
          ))
        ) : (
          <Text style={styles.caption}>이 incident에는 pending local mutation이 없습니다.</Text>
        )}
      </SectionCard>

      <SectionCard title="Audit Timeline">
        {auditQuery.isLoading ? (
          <Text style={styles.caption}>Loading audit records...</Text>
        ) : auditQuery.data?.items.length ? (
          auditQuery.data.items.map(item => (
            <View key={item.id} style={styles.auditRow}>
              <Text style={styles.auditAction}>{item.action}</Text>
              <Text style={styles.auditMeta}>
                {item.actorRole} / {item.result} / {item.createdAt}
              </Text>
              <Text style={styles.auditDetail}>{item.detail}</Text>
            </View>
          ))
        ) : currentIncident.source === 'optimistic' ? (
          <Text style={styles.caption}>
            로컬 optimistic incident는 아직 서버 audit trail을 갖지 않습니다.
          </Text>
        ) : (
          <Text style={styles.caption}>No audit records for this incident.</Text>
        )}
      </SectionCard>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  description: {
    color: theme.color.mutedInk,
    fontSize: 15,
    lineHeight: 22,
  },
  caption: {
    color: theme.color.mutedInk,
    fontSize: 14,
    lineHeight: 20,
  },
  error: {
    color: theme.color.danger,
    fontSize: 14,
  },
  jobRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: theme.spacing.md,
  },
  jobLabel: {
    color: theme.color.ink,
    fontSize: 15,
    fontWeight: '600',
    flex: 1,
  },
  auditRow: {
    paddingVertical: theme.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: theme.color.border,
    gap: 4,
  },
  auditAction: {
    color: theme.color.ink,
    fontSize: 15,
    fontWeight: '700',
  },
  auditMeta: {
    color: theme.color.mutedInk,
    fontSize: 13,
  },
  auditDetail: {
    color: theme.color.ink,
    fontSize: 14,
    lineHeight: 20,
  },
});
