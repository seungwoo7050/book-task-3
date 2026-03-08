import React from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { USER_ROLES } from './contracts';
import {
  acknowledgeIncident,
  decideApproval,
  initialAuditLogs,
  initialIncident,
  listAvailableActions,
  loginAs,
  replayFrom,
  requestResolution,
} from './harnessModel';

export function IncidentOpsHarnessApp(): React.JSX.Element {
  const [actor, setActor] = React.useState(loginAs('REPORTER'));
  const [incident, setIncident] = React.useState(initialIncident);
  const [approval, setApproval] = React.useState<ReturnType<typeof requestResolution>['approval'] | null>(null);
  const [auditLogs, setAuditLogs] = React.useState(initialAuditLogs);
  const [lastEventId, setLastEventId] = React.useState(1);

  const availableActions = listAvailableActions(actor, incident, approval);
  const replayEvents = replayFrom(lastEventId);

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.eyebrow}>Incident Ops Capstone</Text>
        <Text style={styles.title}>Contract Harness</Text>
        <Text style={styles.subtitle}>
          canonical DTO, approval gate, audit log, replay cursor를 작은 RN surface에서 확인합니다.
        </Text>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Login Actor</Text>
          <View style={styles.row}>
            {USER_ROLES.map(role => (
              <Pressable
                key={role}
                testID={`role-button-${role}`}
                onPress={() => setActor(loginAs(role))}
                style={[styles.pill, actor.role === role && styles.pillActive]}>
                <Text style={styles.pillText}>{role}</Text>
              </Pressable>
            ))}
          </View>
          <Text testID="selected-actor" style={styles.meta}>
            {actor.userId} ({actor.role})
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Incident</Text>
          <Text style={styles.incidentTitle}>{incident.title}</Text>
          <Text testID="incident-status" style={styles.meta}>
            status: {incident.status}
          </Text>
          <Text testID="available-actions" style={styles.meta}>
            actions: {availableActions.join(', ') || 'none'}
          </Text>
          <View style={styles.row}>
            <Pressable
              disabled={!availableActions.includes('ack')}
              onPress={() => {
                const next = acknowledgeIncident(incident, actor);
                setIncident(next.incident);
                setAuditLogs(current => [...current, next.auditLog]);
              }}
              style={[styles.actionButton, !availableActions.includes('ack') && styles.actionButtonDisabled]}
              testID="ack-button">
              <Text style={styles.actionText}>Ack</Text>
            </Pressable>
            <Pressable
              disabled={!availableActions.includes('request-resolution')}
              onPress={() => {
                const next = requestResolution(incident, actor);
                setIncident(next.incident);
                setApproval(next.approval);
                setAuditLogs(current => [...current, next.auditLog]);
              }}
              style={[
                styles.actionButton,
                !availableActions.includes('request-resolution') && styles.actionButtonDisabled,
              ]}
              testID="request-resolution-button">
              <Text style={styles.actionText}>Request Resolution</Text>
            </Pressable>
          </View>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Approval</Text>
          <Text testID="approval-status" style={styles.meta}>
            {approval ? approval.status : 'not requested'}
          </Text>
          <View style={styles.row}>
            <Pressable
              disabled={!availableActions.includes('approve') || !approval}
              onPress={() => {
                if (!approval) {
                  return;
                }
                const next = decideApproval(incident, approval, actor, 'APPROVE');
                setIncident(next.incident);
                setApproval(next.approval);
                setAuditLogs(current => [...current, next.auditLog]);
              }}
              style={[styles.actionButton, (!availableActions.includes('approve') || !approval) && styles.actionButtonDisabled]}
              testID="approve-button">
              <Text style={styles.actionText}>Approve</Text>
            </Pressable>
            <Pressable
              disabled={!availableActions.includes('reject') || !approval}
              onPress={() => {
                if (!approval) {
                  return;
                }
                const next = decideApproval(incident, approval, actor, 'REJECT');
                setIncident(next.incident);
                setApproval(next.approval);
                setAuditLogs(current => [...current, next.auditLog]);
              }}
              style={[styles.actionButton, (!availableActions.includes('reject') || !approval) && styles.actionButtonDisabled]}
              testID="reject-button">
              <Text style={styles.actionText}>Reject</Text>
            </Pressable>
          </View>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Audit Timeline</Text>
          {auditLogs.map(log => (
            <Text key={log.id} style={styles.auditItem}>
              #{log.id} {log.action} [{log.result}]
            </Text>
          ))}
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Replay Diagnostics</Text>
          <Text testID="replay-count" style={styles.meta}>
            missed events: {replayEvents.length}
          </Text>
          <Pressable
            onPress={() => setLastEventId(current => Math.min(current + 1, 4))}
            style={styles.actionButton}
            testID="advance-replay-button">
            <Text style={styles.actionText}>Advance Cursor</Text>
          </Pressable>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#eef4f5',
  },
  content: {
    gap: 12,
    padding: 20,
  },
  eyebrow: {
    color: '#3e6467',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#10282a',
    fontSize: 30,
    fontWeight: '800',
  },
  subtitle: {
    color: '#425b5e',
    fontSize: 15,
    lineHeight: 21,
  },
  card: {
    backgroundColor: '#ffffff',
    borderColor: '#d4e2e4',
    borderRadius: 18,
    borderWidth: 1,
    gap: 10,
    padding: 16,
  },
  cardTitle: {
    color: '#10282a',
    fontSize: 20,
    fontWeight: '800',
  },
  row: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  pill: {
    backgroundColor: '#dce9eb',
    borderRadius: 999,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  pillActive: {
    backgroundColor: '#5d8b8e',
  },
  pillText: {
    color: '#10282a',
    fontSize: 13,
    fontWeight: '700',
  },
  meta: {
    color: '#3f5a5d',
    fontSize: 14,
  },
  incidentTitle: {
    color: '#132b2d',
    fontSize: 18,
    fontWeight: '700',
  },
  actionButton: {
    backgroundColor: '#10282a',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  actionButtonDisabled: {
    backgroundColor: '#94a9ac',
  },
  actionText: {
    color: '#ffffff',
    fontSize: 13,
    fontWeight: '700',
  },
  auditItem: {
    color: '#294245',
    fontSize: 13,
  },
});
