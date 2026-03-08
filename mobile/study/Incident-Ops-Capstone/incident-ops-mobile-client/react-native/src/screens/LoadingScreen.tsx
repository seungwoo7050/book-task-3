import React from 'react';
import { ActivityIndicator, Text } from 'react-native';

import { ScreenLayout, SectionCard } from '../components/Ui';
import { theme } from '../theme';

export function LoadingScreen() {
  return (
    <ScreenLayout scroll={false}>
      <SectionCard eyebrow="Boot">
        <ActivityIndicator color={theme.color.accent} size="large" />
        <Text
          style={{
            color: theme.color.ink,
            fontSize: 18,
            fontWeight: '800',
          }}>
          Incident Ops Client
        </Text>
        <Text
          style={{
            color: theme.color.mutedInk,
            fontSize: 15,
            lineHeight: 22,
          }}>
          세션, 설정, outbox, stream cursor를 복구하는 중입니다.
        </Text>
      </SectionCard>
    </ScreenLayout>
  );
}
