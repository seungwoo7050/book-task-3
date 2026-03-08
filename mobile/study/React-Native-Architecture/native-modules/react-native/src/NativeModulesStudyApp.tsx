import React from 'react';
import { SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { MODULE_SPECS } from './specs';

export function NativeModulesStudyApp(): React.JSX.Element {
  return (
    <SafeAreaView style={styles.screen}>
      <Text style={styles.eyebrow}>Architecture</Text>
      <Text style={styles.title}>Native Modules</Text>
      <Text style={styles.subtitle}>
        Battery, Haptics, Sensor 세 모듈의 typed spec과 consumer surface를 같은 화면에 둡니다.
      </Text>

      {MODULE_SPECS.map(spec => (
        <View key={spec.name} style={styles.card}>
          <Text style={styles.cardTitle}>{spec.name}</Text>
          <Text style={styles.cardBody}>{spec.methods.join(' · ')}</Text>
        </View>
      ))}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f5f0eb',
    gap: 12,
    padding: 20,
  },
  eyebrow: {
    color: '#725847',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    color: '#21160f',
    fontSize: 28,
    fontWeight: '800',
  },
  subtitle: {
    color: '#54463b',
    fontSize: 15,
    lineHeight: 21,
  },
  card: {
    backgroundColor: '#fffdf8',
    borderColor: '#e9d7c7',
    borderRadius: 20,
    borderWidth: 1,
    gap: 6,
    padding: 16,
  },
  cardTitle: {
    color: '#21160f',
    fontSize: 20,
    fontWeight: '800',
  },
  cardBody: {
    color: '#56463a',
    fontSize: 14,
  },
});
