import React from 'react';
import { DrawerActions } from '@react-navigation/native';
import type { StackHeaderProps } from '@react-navigation/stack';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { palette } from '../theme';

const titleMap: Record<string, string> = {
  Home: 'Navigation Lab',
  Detail: 'Detail Drill',
  Settings: 'Settings Bridge',
  ProfileDetail: 'Profile Detail',
  ProfileHub: 'Profile Hub',
  EditProfile: 'Edit Profile',
};

export function AppHeader({
  back,
  navigation,
  options,
  route,
}: StackHeaderProps) {
  const title =
    options.title ??
    (typeof options.headerTitle === 'string' ? options.headerTitle : undefined) ??
    titleMap[route.name] ??
    route.name;

  return (
    <View style={styles.shell}>
      <Pressable
        accessibilityRole="button"
        onPress={() => {
          if (back) {
            navigation.goBack();
            return;
          }

          navigation.dispatch(DrawerActions.openDrawer());
        }}
        style={({ pressed }) => [
          styles.leadingButton,
          pressed && styles.pressed,
        ]}
      >
        <Text style={styles.leadingLabel}>{back ? 'Back' : 'Menu'}</Text>
      </Pressable>
      <View style={styles.titleWrap}>
        <Text style={styles.eyebrow}>{route.name}</Text>
        <Text style={styles.title}>{title}</Text>
      </View>
      <View style={styles.modeChip}>
        <Text style={styles.modeChipLabel}>{back ? 'Flow' : 'Root'}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  shell: {
    alignItems: 'center',
    backgroundColor: palette.midnight,
    borderBottomColor: '#1e3555',
    borderBottomWidth: 1,
    flexDirection: 'row',
    paddingBottom: 14,
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  leadingButton: {
    backgroundColor: '#1b2f49',
    borderRadius: 999,
    minWidth: 58,
    paddingHorizontal: 10,
    paddingVertical: 8,
  },
  pressed: {
    opacity: 0.84,
  },
  leadingLabel: {
    color: palette.mist,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.7,
    textAlign: 'center',
    textTransform: 'uppercase',
  },
  titleWrap: {
    flex: 1,
    marginHorizontal: 14,
  },
  eyebrow: {
    color: '#8fb0d7',
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  title: {
    color: '#ffffff',
    fontSize: 19,
    fontWeight: '800',
    marginTop: 4,
  },
  modeChip: {
    backgroundColor: palette.coral,
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 7,
  },
  modeChipLabel: {
    color: '#fffaf4',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.8,
    textTransform: 'uppercase',
  },
});
