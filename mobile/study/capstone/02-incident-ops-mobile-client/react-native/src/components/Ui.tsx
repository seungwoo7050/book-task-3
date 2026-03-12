import React from 'react';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  type StyleProp,
  type TextInputProps,
  type ViewStyle,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { theme } from '../theme';

export function ScreenLayout(input: {
  children: React.ReactNode;
  scroll?: boolean;
  contentStyle?: StyleProp<ViewStyle>;
}) {
  const body = input.scroll ? (
    <ScrollView
      contentContainerStyle={[styles.screenBody, input.contentStyle]}
      keyboardShouldPersistTaps="handled">
      {input.children}
    </ScrollView>
  ) : (
    <View style={[styles.screenBody, input.contentStyle]}>{input.children}</View>
  );

  return <SafeAreaView style={styles.screen}>{body}</SafeAreaView>;
}

export function SectionCard(input: {
  title?: string;
  eyebrow?: string;
  children: React.ReactNode;
}) {
  return (
    <View style={styles.card}>
      {input.eyebrow ? <Text style={styles.eyebrow}>{input.eyebrow}</Text> : null}
      {input.title ? <Text style={styles.cardTitle}>{input.title}</Text> : null}
      <View style={styles.cardBody}>{input.children}</View>
    </View>
  );
}

export function ActionButton(input: {
  label: string;
  onPress: () => void;
  disabled?: boolean;
  tone?: 'solid' | 'ghost' | 'danger';
  testID?: string;
}) {
  const toneStyle =
    input.tone === 'ghost'
      ? styles.buttonGhost
      : input.tone === 'danger'
        ? styles.buttonDanger
        : styles.buttonSolid;

  return (
    <Pressable
      accessibilityRole="button"
      disabled={input.disabled}
      onPress={input.onPress}
      style={({ pressed }) => [
        styles.button,
        toneStyle,
        input.disabled ? styles.buttonDisabled : null,
        pressed ? styles.buttonPressed : null,
      ]}
      testID={input.testID}>
      <Text
        style={[
          styles.buttonText,
          input.tone === 'ghost' ? styles.buttonGhostText : null,
        ]}>
        {input.label}
      </Text>
    </Pressable>
  );
}

export function FieldLabel({ children }: { children: React.ReactNode }) {
  return <Text style={styles.fieldLabel}>{children}</Text>;
}

export function AppTextField(
  input: TextInputProps & {
    label: string;
    errorText?: string | undefined;
    testID?: string;
  },
) {
  return (
    <View style={styles.fieldGroup}>
      <FieldLabel>{input.label}</FieldLabel>
      <TextInput
        {...input}
        placeholderTextColor={theme.color.mutedInk}
        style={[
          styles.textInput,
          input.multiline ? styles.textInputMultiline : null,
        ]}
      />
      {input.errorText ? <Text style={styles.errorText}>{input.errorText}</Text> : null}
    </View>
  );
}

export function MetricRow(input: { label: string; value: string }) {
  return (
    <View style={styles.metricRow}>
      <Text style={styles.metricLabel}>{input.label}</Text>
      <Text style={styles.metricValue}>{input.value}</Text>
    </View>
  );
}

export function EmptyState(input: { title: string; body: string }) {
  return (
    <View style={styles.emptyState}>
      <Text style={styles.emptyTitle}>{input.title}</Text>
      <Text style={styles.emptyBody}>{input.body}</Text>
    </View>
  );
}

export function StatusPill(input: {
  label: string;
  tone?: 'neutral' | 'info' | 'success' | 'warning' | 'danger';
}) {
  const pillStyle =
    input.tone === 'info'
      ? styles.pillInfo
      : input.tone === 'success'
        ? styles.pillSuccess
        : input.tone === 'warning'
          ? styles.pillWarning
          : input.tone === 'danger'
            ? styles.pillDanger
            : styles.pillNeutral;

  return (
    <View style={[styles.pill, pillStyle]}>
      <Text style={styles.pillText}>{input.label}</Text>
    </View>
  );
}

export const sharedStyles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  rowWrap: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },
  gapSm: {
    gap: theme.spacing.sm,
  },
  gapMd: {
    gap: theme.spacing.md,
  },
});

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: theme.color.background,
  },
  screenBody: {
    flexGrow: 1,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  card: {
    backgroundColor: theme.color.card,
    borderRadius: theme.radius.md,
    padding: theme.spacing.md,
    borderWidth: 1,
    borderColor: theme.color.border,
    gap: theme.spacing.xs,
  },
  eyebrow: {
    color: theme.color.accent,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  cardTitle: {
    color: theme.color.ink,
    fontSize: 20,
    fontWeight: '800',
  },
  cardBody: {
    gap: theme.spacing.sm,
  },
  button: {
    minHeight: 44,
    borderRadius: 999,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
  },
  buttonSolid: {
    backgroundColor: theme.color.ink,
  },
  buttonGhost: {
    backgroundColor: theme.color.cardMuted,
    borderWidth: 1,
    borderColor: theme.color.border,
  },
  buttonDanger: {
    backgroundColor: theme.color.danger,
  },
  buttonDisabled: {
    opacity: 0.45,
  },
  buttonPressed: {
    transform: [{ scale: 0.98 }],
  },
  buttonText: {
    color: theme.color.panel,
    fontSize: 15,
    fontWeight: '700',
  },
  buttonGhostText: {
    color: theme.color.ink,
  },
  fieldGroup: {
    gap: theme.spacing.xs,
  },
  fieldLabel: {
    color: theme.color.ink,
    fontSize: 14,
    fontWeight: '700',
  },
  textInput: {
    minHeight: 48,
    borderRadius: theme.radius.sm,
    borderWidth: 1,
    borderColor: theme.color.border,
    backgroundColor: theme.color.panel,
    color: theme.color.ink,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    fontSize: 15,
  },
  textInputMultiline: {
    minHeight: 108,
    textAlignVertical: 'top',
  },
  errorText: {
    color: theme.color.danger,
    fontSize: 13,
  },
  metricRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: theme.spacing.md,
  },
  metricLabel: {
    color: theme.color.mutedInk,
    fontSize: 14,
  },
  metricValue: {
    color: theme.color.ink,
    fontSize: 14,
    fontWeight: '700',
    flexShrink: 1,
    textAlign: 'right',
  },
  emptyState: {
    paddingVertical: theme.spacing.xl,
    gap: theme.spacing.xs,
  },
  emptyTitle: {
    color: theme.color.ink,
    fontSize: 18,
    fontWeight: '800',
  },
  emptyBody: {
    color: theme.color.mutedInk,
    fontSize: 15,
    lineHeight: 21,
  },
  pill: {
    alignSelf: 'flex-start',
    borderRadius: 999,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: 4,
  },
  pillNeutral: {
    backgroundColor: theme.color.cardMuted,
  },
  pillInfo: {
    backgroundColor: theme.color.infoMuted,
  },
  pillSuccess: {
    backgroundColor: theme.color.successMuted,
  },
  pillWarning: {
    backgroundColor: theme.color.warningMuted,
  },
  pillDanger: {
    backgroundColor: theme.color.dangerMuted,
  },
  pillText: {
    color: theme.color.ink,
    fontSize: 12,
    fontWeight: '700',
  },
});
