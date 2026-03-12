import type { BottomTabScreenProps } from '@react-navigation/bottom-tabs';
import type { DrawerScreenProps } from '@react-navigation/drawer';
import type { NavigatorScreenParams } from '@react-navigation/native';
import type { StackScreenProps } from '@react-navigation/stack';

export type HomeStackParamList = {
  Home: undefined;
  Detail: { id: string; title: string };
  Settings: undefined;
  ProfileDetail: { userId: string };
};

export type ProfileStackParamList = {
  ProfileHub: { userId: string };
  EditProfile: undefined;
};

export type RootTabParamList = {
  HomeTab: NavigatorScreenParams<HomeStackParamList>;
  SearchTab: undefined;
  ProfileTab: NavigatorScreenParams<ProfileStackParamList>;
};

export type RootDrawerParamList = {
  Main: NavigatorScreenParams<RootTabParamList>;
  Notifications: undefined;
  About: undefined;
};

export type RootStackParamList = {
  Drawer: NavigatorScreenParams<RootDrawerParamList>;
  NotFound: undefined;
};

export type HomeScreenProps = StackScreenProps<HomeStackParamList, 'Home'>;
export type DetailScreenProps = StackScreenProps<HomeStackParamList, 'Detail'>;
export type SettingsScreenProps = StackScreenProps<
  HomeStackParamList,
  'Settings'
>;
export type ProfileDetailScreenProps = StackScreenProps<
  HomeStackParamList,
  'ProfileDetail'
>;
export type SearchScreenProps = BottomTabScreenProps<
  RootTabParamList,
  'SearchTab'
>;
export type ProfileHubScreenProps = StackScreenProps<
  ProfileStackParamList,
  'ProfileHub'
>;
export type EditProfileScreenProps = StackScreenProps<
  ProfileStackParamList,
  'EditProfile'
>;
export type NotificationsScreenProps = DrawerScreenProps<
  RootDrawerParamList,
  'Notifications'
>;
export type AboutScreenProps = DrawerScreenProps<RootDrawerParamList, 'About'>;
export type NotFoundScreenProps = StackScreenProps<
  RootStackParamList,
  'NotFound'
>;
