import React from 'react';
import { SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { RUNS, computeStats } from './benchmark';

export function BridgeVsJsiStudyApp(): React.JSX.Element {
  const stats = RUNS.map(computeStats);

  return (
    <SafeAreaView style={styles.screen}>
      <Text style={styles.eyebrow}>Architecture</Text>
      <Text style={styles.title}>Bridge Vs JSI</Text>
      <Text style={styles.subtitle}>
        RN 0.84 기준에서 async serialized surface와 sync direct-call surface를 비교합니다.
      </Text>

      {stats.map(stat => (
        <View key={stat.label} style={styles.card}>
          <Text style={styles.cardTitle}>{stat.label}</Text>
          <Text style={styles.cardBody}>payload: {stat.payloadSize}</Text>
          <Text style={styles.cardBody}>mean: {stat.mean}ms</Text>
          <Text style={styles.cardBody}>stddev: {stat.stddev}ms</Text>
        </View>
      ))}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f7f1eb',
    gap: 12,
    padding: 20,
  },
  eyebrow: {
    color: '#735541',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#20150f',
    fontSize: 28,
    fontWeight: '800',
  },
  subtitle: {
    color: '#5a473b',
    fontSize: 15,
    lineHeight: 21,
  },
  card: {
    backgroundColor: '#fffdf8',
    borderColor: '#ead8ca',
    borderRadius: 20,
    borderWidth: 1,
    gap: 4,
    padding: 16,
  },
  cardTitle: {
    color: '#20150f',
    fontSize: 20,
    fontWeight: '800',
  },
  cardBody: {
    color: '#4e4036',
    fontSize: 14,
  },
});
