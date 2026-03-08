import React, { useState } from 'react';
import {
  DrawerActions,
} from '@react-navigation/native';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import type {
  AboutScreenProps,
  DetailScreenProps,
  EditProfileScreenProps,
  HomeScreenProps,
  NotFoundScreenProps,
  NotificationsScreenProps,
  ProfileDetailScreenProps,
  ProfileHubScreenProps,
  SearchScreenProps,
  SettingsScreenProps,
} from '../navigation/types';
import { palette } from '../theme';

type ScreenShellProps = {
  accent: string;
  eyebrow: string;
  title: string;
  description: string;
  children: React.ReactNode;
};

type ActionButtonProps = {
  label: string;
  onPress: () => void;
  tone?: 'primary' | 'secondary' | 'quiet';
};

function ScreenShell({
  accent,
  eyebrow,
  title,
  description,
  children,
}: ScreenShellProps) {
  return (
    <ScrollView
      contentContainerStyle={styles.screenContent}
      style={styles.screen}
    >
      <View style={[styles.hero, { borderTopColor: accent }]}>
        <Text style={styles.eyebrow}>{eyebrow}</Text>
        <Text accessibilityRole="header" style={styles.heroTitle}>
          {title}
        </Text>
        <Text style={styles.heroDescription}>{description}</Text>
      </View>
      {children}
    </ScrollView>
  );
}

function ActionButton({
  label,
  onPress,
  tone = 'primary',
}: ActionButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [
        styles.actionButton,
        tone === 'secondary' && styles.secondaryButton,
        tone === 'quiet' && styles.quietButton,
        pressed && styles.pressed,
      ]}
    >
      <Text
        style={[
          styles.actionButtonLabel,
          tone === 'quiet' && styles.quietButtonLabel,
        ]}
      >
        {label}
      </Text>
    </Pressable>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.statCard}>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={styles.statValue}>{value}</Text>
    </View>
  );
}

export function HomeScreen({ navigation }: HomeScreenProps) {
  return (
    <ScreenShell
      accent={palette.coral}
      description="Stack, Tab, Drawer가 하나의 navigation state 안에서 어떻게 중첩되는지 확인하는 시작점이다."
      eyebrow="Stack Entry"
      title="Home screen"
    >
      <View style={styles.statGrid}>
        <StatCard label="Tabs" value="3" />
        <StatCard label="Drawer Items" value="4+" />
        <StatCard label="Deep Links" value="5" />
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Explore the flow</Text>
        <Text style={styles.cardBody}>
          Detail screen은 vertical card transition을 사용하고, drawer는 custom
          content와 conditional actions를 가진다.
        </Text>
        <ActionButton
          label="Open detail example"
          onPress={() =>
            navigation.navigate('Detail', {
              id: 'abc123',
              title: 'On-call deep link drill',
            })
          }
        />
        <ActionButton
          label="Open drawer menu"
          onPress={() =>
            navigation.getParent()?.getParent()?.dispatch(DrawerActions.openDrawer())
          }
          tone="secondary"
        />
      </View>
    </ScreenShell>
  );
}

export function DetailScreen({ navigation, route }: DetailScreenProps) {
  return (
    <ScreenShell
      accent={palette.gold}
      description="`detail/:id` 링크는 nested navigator state를 구성한 뒤 이 화면으로 도착한다."
      eyebrow="Deep Link Target"
      title={route.params.title}
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Route params</Text>
        <Text style={styles.codeLine}>id: {route.params.id}</Text>
        <Text style={styles.codeLine}>title: {route.params.title}</Text>
      </View>
      <ActionButton
        label="Continue to settings"
        onPress={() => navigation.navigate('Settings')}
      />
    </ScreenShell>
  );
}

export function SettingsScreen({ navigation }: SettingsScreenProps) {
  return (
    <ScreenShell
      accent={palette.teal}
      description="Header customization과 typed params 전달을 확인하는 중간 단계다."
      eyebrow="Stack Step"
      title="Settings screen"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Typed navigation params</Text>
        <Text style={styles.cardBody}>
          Settings screen은 다음 화면으로 `userId`를 전달한다. 잘못된 shape은
          TypeScript에서 막는다.
        </Text>
      </View>
      <ActionButton
        label="Open profile detail"
        onPress={() =>
          navigation.navigate('ProfileDetail', { userId: 'operator-24' })
        }
      />
    </ScreenShell>
  );
}

export function ProfileDetailScreen({
  route,
}: ProfileDetailScreenProps) {
  return (
    <ScreenShell
      accent={palette.coral}
      description="Home stack 안의 네 번째 화면으로, typed params가 최종 소비되는 지점을 보여 준다."
      eyebrow="Stack Final Step"
      title="Profile detail"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Resolved user</Text>
        <Text style={styles.codeLine}>userId: {route.params.userId}</Text>
      </View>
    </ScreenShell>
  );
}

export function SearchScreen({ navigation }: SearchScreenProps) {
  const [draft, setDraft] = useState('drawer tab state');
  const [tapCount, setTapCount] = useState(1);

  return (
    <ScreenShell
      accent={palette.teal}
      description="탭 전환 중에도 로컬 UI 상태가 유지되는지 확인하는 공간이다."
      eyebrow="Tab Screen"
      title="Search tab"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Stateful tab content</Text>
        <Text style={styles.cardBody}>
          버튼을 눌러 카운트를 늘리고 다른 탭으로 이동한 뒤 돌아와 보라.
        </Text>
        <TextInput
          onChangeText={setDraft}
          placeholder="Search draft"
          placeholderTextColor="#7890a8"
          style={styles.input}
          value={draft}
        />
        <Text style={styles.codeLine}>tapCount: {tapCount}</Text>
        <ActionButton
          label="Increment local counter"
          onPress={() => setTapCount(current => current + 1)}
        />
        <ActionButton
          label="Open drawer from tab"
          onPress={() =>
            navigation.getParent()?.dispatch(DrawerActions.openDrawer())
          }
          tone="quiet"
        />
      </View>
    </ScreenShell>
  );
}

export function ProfileHubScreen({
  navigation,
  route,
}: ProfileHubScreenProps) {
  return (
    <ScreenShell
      accent={palette.gold}
      description="`profile/:userId` deep link의 기본 목적지다."
      eyebrow="Profile Tab"
      title="Profile hub"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Active account</Text>
        <Text style={styles.codeLine}>userId: {route.params.userId}</Text>
      </View>
      <ActionButton
        label="Edit profile details"
        onPress={() => navigation.navigate('EditProfile')}
      />
    </ScreenShell>
  );
}

export function EditProfileScreen({
  navigation,
}: EditProfileScreenProps) {
  return (
    <ScreenShell
      accent={palette.coral}
      description="Profile tab 안의 독립 stack을 유지한 채 편집 화면으로 진입한다."
      eyebrow="Profile Stack"
      title="Edit profile"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Mock editor</Text>
        <Text style={styles.cardBody}>
          실제 저장 로직 대신 navigation flow와 header behavior를 보여 주는 데
          집중한다.
        </Text>
      </View>
      <ActionButton
        label="Return to profile hub"
        onPress={() => navigation.goBack()}
      />
    </ScreenShell>
  );
}

export function NotificationsScreen({
  navigation,
}: NotificationsScreenProps) {
  return (
    <ScreenShell
      accent={palette.coral}
      description="Drawer 레벨에서 직접 접근하는 독립 화면이다."
      eyebrow="Drawer Screen"
      title="Notifications"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Notification queue</Text>
        <Text style={styles.cardBody}>
          Drawer action과 screen navigation이 같은 커스텀 메뉴에 공존한다.
        </Text>
      </View>
      <ActionButton
        label="Back to main tabs"
        onPress={() =>
          navigation.navigate('Main', {
            screen: 'HomeTab',
            params: { screen: 'Home' },
          })
        }
      />
    </ScreenShell>
  );
}

export function AboutScreen({ navigation }: AboutScreenProps) {
  return (
    <ScreenShell
      accent={palette.teal}
      description="이 화면은 앱 구조와 deep link 테스트 경로를 설명한다."
      eyebrow="Drawer Screen"
      title="About"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Quick links</Text>
        <Text style={styles.codeLine}>myapp://home</Text>
        <Text style={styles.codeLine}>myapp://detail/abc123</Text>
        <Text style={styles.codeLine}>myapp://profile/user42</Text>
      </View>
      <ActionButton
        label="Return to main tabs"
        onPress={() =>
          navigation.navigate('Main', {
            screen: 'HomeTab',
            params: { screen: 'Home' },
          })
        }
      />
    </ScreenShell>
  );
}

export function NotFoundScreen({ navigation }: NotFoundScreenProps) {
  return (
    <ScreenShell
      accent={palette.gold}
      description="알 수 없는 deep link는 여기로 라우팅된다."
      eyebrow="Fallback"
      title="Not found"
    >
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Unknown route</Text>
        <Text style={styles.cardBody}>
          등록되지 않은 path는 wildcard fallback이 처리한다.
        </Text>
      </View>
      <ActionButton
        label="Go home"
        onPress={() =>
          navigation.navigate('Drawer', {
            screen: 'Main',
            params: {
              screen: 'HomeTab',
              params: { screen: 'Home' },
            },
          })
        }
      />
    </ScreenShell>
  );
}

const styles = StyleSheet.create({
  screen: {
    backgroundColor: palette.panel,
    flex: 1,
  },
  screenContent: {
    gap: 16,
    padding: 20,
  },
  hero: {
    backgroundColor: '#ffffff',
    borderRadius: 28,
    borderTopWidth: 10,
    elevation: 3,
    padding: 22,
    shadowColor: palette.shadow,
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.09,
    shadowRadius: 18,
  },
  eyebrow: {
    color: palette.slate,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  heroTitle: {
    color: palette.ink,
    fontSize: 30,
    fontWeight: '800',
    marginTop: 8,
  },
  heroDescription: {
    color: '#51657d',
    fontSize: 15,
    lineHeight: 22,
    marginTop: 10,
  },
  statGrid: {
    flexDirection: 'row',
    gap: 12,
  },
  statCard: {
    backgroundColor: '#dff3f0',
    borderRadius: 22,
    flex: 1,
    padding: 16,
  },
  statLabel: {
    color: '#3d566f',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.6,
    textTransform: 'uppercase',
  },
  statValue: {
    color: palette.midnight,
    fontSize: 24,
    fontWeight: '800',
    marginTop: 10,
  },
  card: {
    backgroundColor: '#ffffff',
    borderColor: '#e3edf7',
    borderRadius: 24,
    borderWidth: 1,
    gap: 12,
    padding: 20,
  },
  cardTitle: {
    color: palette.ink,
    fontSize: 18,
    fontWeight: '800',
  },
  cardBody: {
    color: '#4d6278',
    fontSize: 15,
    lineHeight: 22,
  },
  actionButton: {
    backgroundColor: palette.midnight,
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 14,
  },
  secondaryButton: {
    backgroundColor: palette.coral,
  },
  quietButton: {
    backgroundColor: '#eef4fb',
  },
  actionButtonLabel: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '700',
    textAlign: 'center',
  },
  quietButtonLabel: {
    color: palette.ink,
  },
  pressed: {
    opacity: 0.86,
  },
  codeLine: {
    color: palette.slate,
    fontSize: 14,
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#f8fbff',
    borderColor: '#cad7e4',
    borderRadius: 16,
    borderWidth: 1,
    color: palette.ink,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
});
