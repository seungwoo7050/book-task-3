import React, { useMemo, useState } from 'react';
import {
  createDrawerNavigator,
  DrawerContentScrollView,
  DrawerItem,
  type DrawerContentComponentProps,
} from '@react-navigation/drawer';
import {
  DrawerActions,
  type NavigatorScreenParams,
} from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import {
  CardStyleInterpolators,
  createStackNavigator,
  TransitionSpecs,
  type StackCardInterpolationProps,
  type StackNavigationOptions,
} from '@react-navigation/stack';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { AppHeader } from '../components/AppHeader';
import {
  AboutScreen,
  DetailScreen,
  EditProfileScreen,
  HomeScreen,
  NotFoundScreen,
  NotificationsScreen,
  ProfileDetailScreen,
  ProfileHubScreen,
  SearchScreen,
  SettingsScreen,
} from '../screens/AppScreens';
import { palette } from '../theme';
import type {
  HomeStackParamList,
  ProfileStackParamList,
  RootDrawerParamList,
  RootStackParamList,
  RootTabParamList,
} from './types';

const RootStack = createStackNavigator<RootStackParamList>();
const Drawer = createDrawerNavigator<RootDrawerParamList>();
const Tabs = createBottomTabNavigator<RootTabParamList>();
const HomeStack = createStackNavigator<HomeStackParamList>();
const ProfileStack = createStackNavigator<ProfileStackParamList>();

const detailTransition: StackNavigationOptions = {
  gestureDirection: 'vertical',
  transitionSpec: {
    open: TransitionSpecs.TransitionIOSSpec,
    close: TransitionSpecs.TransitionIOSSpec,
  },
  cardStyleInterpolator: ({
    current,
    layouts,
  }: StackCardInterpolationProps) => ({
    cardStyle: {
      opacity: current.progress.interpolate({
        inputRange: [0, 1],
        outputRange: [0.82, 1],
      }),
      transform: [
        {
          translateY: current.progress.interpolate({
            inputRange: [0, 1],
            outputRange: [layouts.screen.height, 0],
          }),
        },
      ],
    },
  }),
};

type SessionState = {
  isSignedIn: boolean;
  notificationCount: number;
};

function HomeStackNavigator() {
  return (
    <HomeStack.Navigator
      screenOptions={{
        cardStyle: { backgroundColor: palette.panel },
        header: props => <AppHeader {...props} />,
      }}
    >
      <HomeStack.Screen component={HomeScreen} name="Home" />
      <HomeStack.Screen
        component={DetailScreen}
        name="Detail"
        options={detailTransition}
      />
      <HomeStack.Screen component={SettingsScreen} name="Settings" />
      <HomeStack.Screen
        component={ProfileDetailScreen}
        name="ProfileDetail"
        options={{
          cardStyleInterpolator: CardStyleInterpolators.forFadeFromCenter,
        }}
      />
    </HomeStack.Navigator>
  );
}

function ProfileStackNavigator() {
  return (
    <ProfileStack.Navigator
      screenOptions={{
        cardStyle: { backgroundColor: palette.panel },
        header: props => <AppHeader {...props} />,
      }}
    >
      <ProfileStack.Screen
        component={ProfileHubScreen}
        initialParams={{ userId: 'designer-07' }}
        name="ProfileHub"
      />
      <ProfileStack.Screen component={EditProfileScreen} name="EditProfile" />
    </ProfileStack.Navigator>
  );
}

function TabIcon({
  focused,
  glyph,
}: {
  focused: boolean;
  glyph: string;
}) {
  return (
    <View style={[styles.iconShell, focused && styles.iconShellFocused]}>
      <Text style={[styles.iconGlyph, focused && styles.iconGlyphFocused]}>
        {glyph}
      </Text>
    </View>
  );
}

function MainTabs({
  notificationCount,
}: {
  notificationCount: number;
}) {
  return (
    <Tabs.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        lazy: true,
        tabBarActiveTintColor: palette.coral,
        tabBarInactiveTintColor: '#6f8398',
        tabBarLabelStyle: styles.tabBarLabel,
        tabBarStyle: styles.tabBar,
        tabBarIcon: ({ focused }) => {
          if (route.name === 'HomeTab') {
            return <TabIcon focused={focused} glyph="◎" />;
          }

          if (route.name === 'SearchTab') {
            return <TabIcon focused={focused} glyph="◇" />;
          }

          return <TabIcon focused={focused} glyph="▲" />;
        },
      })}
    >
      <Tabs.Screen
        component={HomeStackNavigator}
        name="HomeTab"
        options={{ title: 'Home' }}
      />
      <Tabs.Screen
        component={SearchScreen}
        name="SearchTab"
        options={{
          tabBarBadge: notificationCount,
          title: 'Search',
        }}
      />
      <Tabs.Screen
        component={ProfileStackNavigator}
        name="ProfileTab"
        options={{ title: 'Profile' }}
      />
    </Tabs.Navigator>
  );
}

function navigateToHome(
  navigation: DrawerContentComponentProps['navigation'],
  params?: NavigatorScreenParams<RootTabParamList>,
) {
  navigation.navigate('Main', params ?? { screen: 'HomeTab' });
}

function CustomDrawerContent({
  navigation,
  onSignIn,
  onSignOut,
  session,
}: DrawerContentComponentProps & {
  onSignIn: () => void;
  onSignOut: () => void;
  session: SessionState;
}) {
  return (
    <DrawerContentScrollView
      contentContainerStyle={styles.drawerContent}
      scrollEnabled={false}
    >
      <View style={styles.drawerHero}>
        <Text style={styles.drawerEyebrow}>Navigation Study</Text>
        <Text style={styles.drawerTitle}>Nested navigation lab</Text>
        <Text style={styles.drawerBody}>
          Custom drawer content controls both screen navigation and stateful
          actions.
        </Text>
        <View style={styles.sessionChip}>
          <Text style={styles.sessionChipLabel}>
            {session.isSignedIn ? 'Signed in' : 'Signed out'}
          </Text>
        </View>
      </View>

      <DrawerItem
        focused={false}
        inactiveTintColor={palette.ink}
        label="Main tabs"
        onPress={() => navigateToHome(navigation)}
        style={styles.drawerItem}
      />
      {session.isSignedIn ? (
        <DrawerItem
          focused={false}
          inactiveTintColor={palette.ink}
          label={`Notifications (${session.notificationCount})`}
          onPress={() => navigation.navigate('Notifications')}
          style={styles.drawerItem}
        />
      ) : null}
      <DrawerItem
        focused={false}
        inactiveTintColor={palette.ink}
        label="About"
        onPress={() => navigation.navigate('About')}
        style={styles.drawerItem}
      />
      {session.isSignedIn ? (
        <DrawerItem
          focused={false}
          inactiveTintColor={palette.coral}
          label="Log out"
          onPress={() => {
            onSignOut();
            navigateToHome(navigation);
          }}
          style={styles.drawerItem}
        />
      ) : (
        <DrawerItem
          focused={false}
          inactiveTintColor={palette.teal}
          label="Sign in"
          onPress={() => {
            onSignIn();
            navigateToHome(navigation, {
              screen: 'ProfileTab',
              params: {
                params: { userId: 'designer-07' },
                screen: 'ProfileHub',
              },
            });
          }}
          style={styles.drawerItem}
        />
      )}
      <Pressable
        onPress={() => navigation.dispatch(DrawerActions.closeDrawer())}
        style={({ pressed }) => [
          styles.drawerFooterButton,
          pressed && styles.pressed,
        ]}
      >
        <Text style={styles.drawerFooterLabel}>Close drawer</Text>
      </Pressable>
    </DrawerContentScrollView>
  );
}

function DrawerNavigator() {
  const [session, setSession] = useState<SessionState>({
    isSignedIn: true,
    notificationCount: 3,
  });

  const drawerContent = useMemo(
    () =>
      (props: DrawerContentComponentProps) =>
        (
          <CustomDrawerContent
            {...props}
            onSignIn={() =>
              setSession(current => ({ ...current, isSignedIn: true }))
            }
            onSignOut={() =>
              setSession(current => ({ ...current, isSignedIn: false }))
            }
            session={session}
          />
        ),
    [session],
  );

  return (
    <Drawer.Navigator
      drawerContent={drawerContent}
      screenOptions={{
        drawerStyle: styles.drawerShell,
        drawerType: 'front',
        headerStyle: styles.drawerHeader,
        headerTintColor: '#ffffff',
        headerTitleStyle: styles.drawerHeaderTitle,
      }}
    >
      <Drawer.Screen
        name="Main"
        options={{ headerShown: false, title: 'Main tabs' }}
      >
        {() => <MainTabs notificationCount={session.notificationCount} />}
      </Drawer.Screen>
      <Drawer.Screen component={NotificationsScreen} name="Notifications" />
      <Drawer.Screen component={AboutScreen} name="About" />
    </Drawer.Navigator>
  );
}

export function RootNavigator() {
  return (
    <RootStack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <RootStack.Screen component={DrawerNavigator} name="Drawer" />
      <RootStack.Screen
        component={NotFoundScreen}
        name="NotFound"
        options={{ presentation: 'modal' }}
      />
    </RootStack.Navigator>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: '#ffffff',
    borderTopWidth: 0,
    elevation: 0,
    height: 82,
    paddingBottom: 10,
    paddingTop: 10,
    shadowColor: palette.shadow,
    shadowOffset: { width: 0, height: -6 },
    shadowOpacity: 0.12,
    shadowRadius: 20,
  },
  tabBarLabel: {
    fontSize: 12,
    fontWeight: '700',
  },
  iconShell: {
    alignItems: 'center',
    backgroundColor: '#edf3fa',
    borderRadius: 17,
    height: 34,
    justifyContent: 'center',
    width: 34,
  },
  iconShellFocused: {
    backgroundColor: '#ffe1d7',
  },
  iconGlyph: {
    color: '#6c8198',
    fontSize: 16,
    fontWeight: '700',
  },
  iconGlyphFocused: {
    color: palette.coral,
  },
  drawerShell: {
    backgroundColor: '#f5f9fd',
    width: 310,
  },
  drawerHeader: {
    backgroundColor: palette.midnight,
  },
  drawerHeaderTitle: {
    fontWeight: '800',
  },
  drawerContent: {
    flex: 1,
    justifyContent: 'space-between',
    padding: 18,
  },
  drawerHero: {
    backgroundColor: '#ffffff',
    borderRadius: 26,
    borderTopColor: palette.coral,
    borderTopWidth: 9,
    marginBottom: 16,
    padding: 20,
  },
  drawerEyebrow: {
    color: '#637b95',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.8,
    textTransform: 'uppercase',
  },
  drawerTitle: {
    color: palette.ink,
    fontSize: 24,
    fontWeight: '800',
    marginTop: 8,
  },
  drawerBody: {
    color: '#4e657f',
    fontSize: 14,
    lineHeight: 21,
    marginTop: 10,
  },
  sessionChip: {
    alignSelf: 'flex-start',
    backgroundColor: '#dff5ec',
    borderRadius: 999,
    marginTop: 14,
    paddingHorizontal: 10,
    paddingVertical: 7,
  },
  sessionChipLabel: {
    color: '#167a68',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.8,
    textTransform: 'uppercase',
  },
  drawerItem: {
    borderRadius: 18,
    marginVertical: 2,
  },
  drawerFooterButton: {
    backgroundColor: palette.midnight,
    borderRadius: 18,
    marginTop: 'auto',
    paddingHorizontal: 18,
    paddingVertical: 14,
  },
  drawerFooterLabel: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '800',
    textAlign: 'center',
  },
  pressed: {
    opacity: 0.86,
  },
});
