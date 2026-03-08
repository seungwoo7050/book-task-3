import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { useAppModel } from '../app/AppModel';
import { theme } from '../theme';
import type {
  AuthStackParamList,
  IncidentStackParamList,
  MainTabParamList,
} from './types';
import { ApprovalsScreen } from '../screens/ApprovalsScreen';
import { CreateIncidentScreen } from '../screens/CreateIncidentScreen';
import { IncidentDetailScreen } from '../screens/IncidentDetailScreen';
import { IncidentsScreen } from '../screens/IncidentsScreen';
import { LoadingScreen } from '../screens/LoadingScreen';
import { LoginScreen } from '../screens/LoginScreen';
import { OutboxScreen } from '../screens/OutboxScreen';
import { SettingsScreen } from '../screens/SettingsScreen';

const AuthStack = createNativeStackNavigator<AuthStackParamList>();
const IncidentStack = createNativeStackNavigator<IncidentStackParamList>();
const Tabs = createBottomTabNavigator<MainTabParamList>();

function IncidentStackScreen() {
  return (
    <IncidentStack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.color.panel,
        },
        headerTintColor: theme.color.ink,
        headerTitleStyle: {
          fontWeight: '800',
        },
        contentStyle: {
          backgroundColor: theme.color.background,
        },
      }}>
      <IncidentStack.Screen
        component={IncidentsScreen}
        name="IncidentFeed"
        options={{ title: 'Incidents' }}
      />
      <IncidentStack.Screen
        component={CreateIncidentScreen}
        name="CreateIncident"
        options={{ title: 'Create Incident' }}
      />
      <IncidentStack.Screen
        component={IncidentDetailScreen}
        name="IncidentDetail"
        options={{ title: 'Incident Detail' }}
      />
    </IncidentStack.Navigator>
  );
}

function MainTabs() {
  return (
    <Tabs.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.color.panel,
        },
        headerTintColor: theme.color.ink,
        headerTitleStyle: {
          fontWeight: '800',
        },
        tabBarStyle: {
          backgroundColor: theme.color.panel,
          borderTopColor: theme.color.border,
          minHeight: 64,
          paddingTop: 6,
        },
        tabBarActiveTintColor: theme.color.accent,
        tabBarInactiveTintColor: theme.color.mutedInk,
      }}>
      <Tabs.Screen
        component={IncidentStackScreen}
        name="IncidentsTab"
        options={{ headerShown: false, title: 'Incidents' }}
      />
      <Tabs.Screen
        component={ApprovalsScreen}
        name="Approvals"
        options={{ title: 'Approvals' }}
      />
      <Tabs.Screen
        component={OutboxScreen}
        name="Outbox"
        options={{ title: 'Outbox' }}
      />
      <Tabs.Screen
        component={SettingsScreen}
        name="Settings"
        options={{ title: 'Settings' }}
      />
    </Tabs.Navigator>
  );
}

export function RootNavigator() {
  const { bootstrapState, session } = useAppModel();

  return (
    <NavigationContainer>
      {bootstrapState !== 'ready' ? (
        <LoadingScreen />
      ) : session ? (
        <MainTabs />
      ) : (
        <AuthStack.Navigator
          screenOptions={{
            headerShown: false,
            contentStyle: {
              backgroundColor: theme.color.background,
            },
          }}>
          <AuthStack.Screen component={LoginScreen} name="Login" />
        </AuthStack.Navigator>
      )}
    </NavigationContainer>
  );
}
