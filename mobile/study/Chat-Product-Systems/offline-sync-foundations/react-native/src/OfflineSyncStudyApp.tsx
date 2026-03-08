import React, { useState } from 'react';
import { Pressable, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { FakeSyncServer, createTaskDraft, flushQueue } from './syncEngine';

type Section = 'Tasks' | 'Outbox' | 'DLQ' | 'Diagnostics';

const seeded = [createTaskDraft('Investigate queue', 1), createTaskDraft('FAIL replay', 2)];
const snapshot = flushQueue(
  seeded.map(entry => entry.task),
  seeded.map(entry => entry.job),
  new FakeSyncServer(),
);

export function OfflineSyncStudyApp(): React.JSX.Element {
  const [section, setSection] = useState<Section>('Tasks');
  const outboxCount = snapshot.jobs.filter(job => job.state !== 'synced').length;
  const dlqCount = snapshot.jobs.filter(job => job.state === 'dlq').length;

  return (
    <SafeAreaView style={styles.screen}>
      <Text style={styles.eyebrow}>Chat Product Systems</Text>
      <Text style={styles.title}>Offline Sync Foundations</Text>
      <Text style={styles.subtitle}>
        create queue, retry, DLQ, idempotency, merge 규칙을 deterministic fake server로 검증합니다.
      </Text>

      <View style={styles.row}>
        {(['Tasks', 'Outbox', 'DLQ', 'Diagnostics'] as Section[]).map(item => (
          <Pressable
            key={item}
            accessibilityRole="button"
            onPress={() => setSection(item)}
            style={[styles.chip, section === item && styles.chipActive]}>
            <Text style={[styles.chipLabel, section === item && styles.chipLabelActive]}>
              {item}
            </Text>
          </Pressable>
        ))}
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>{section}</Text>
        <Text style={styles.cardBody}>tasks: {snapshot.tasks.length}</Text>
        <Text style={styles.cardBody}>outbox: {outboxCount}</Text>
        <Text style={styles.cardBody}>dlq: {dlqCount}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f4efe7',
    gap: 12,
    padding: 20,
  },
  eyebrow: {
    color: '#785741',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#20140e',
    fontSize: 28,
    fontWeight: '800',
  },
  subtitle: {
    color: '#56453b',
    fontSize: 15,
    lineHeight: 21,
  },
  row: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    borderColor: '#c8b7ab',
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  chipActive: {
    backgroundColor: '#20140e',
    borderColor: '#20140e',
  },
  chipLabel: {
    color: '#4f4037',
    fontWeight: '700',
  },
  chipLabelActive: {
    color: '#fdf8f1',
  },
  card: {
    backgroundColor: '#fffdf8',
    borderColor: '#e8d8c9',
    borderRadius: 20,
    borderWidth: 1,
    gap: 6,
    padding: 16,
  },
  cardTitle: {
    color: '#20140e',
    fontSize: 20,
    fontWeight: '800',
  },
  cardBody: {
    color: '#5a473b',
    fontSize: 14,
  },
});
