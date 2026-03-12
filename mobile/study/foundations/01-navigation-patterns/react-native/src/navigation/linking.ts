import {
  getStateFromPath,
  type InitialState,
  type LinkingOptions,
} from '@react-navigation/native';

import type { RootStackParamList } from './types';

type RouteNode = {
  name: string;
  params?: Record<string, unknown>;
  state?: RouteState;
};

type RouteState = {
  routes: RouteNode[];
};

type MaybeState = RouteState | undefined;

const normalizePath = (input: string) =>
  input
    .replace(/^myapp:\/\//, '')
    .replace(/^https:\/\/myapp\.example\.com\/?/, '')
    .replace(/^\//, '');

const visitRoutes = (
  state: MaybeState,
  visitor: (route: RouteNode) => void,
): void => {
  if (!state) {
    return;
  }

  state.routes.forEach(route => {
    visitor(route);

    visitRoutes(route.state, visitor);
  });
};

const buildDetailTitle = (id: string) =>
  `Detail route for ${id.replace(/[-_]/g, ' ')}`;

export const linking: LinkingOptions<RootStackParamList> = {
  prefixes: ['myapp://', 'https://myapp.example.com'],
  config: {
    screens: {
      Drawer: {
        screens: {
          Main: {
            screens: {
              HomeTab: {
                screens: {
                  Home: 'home',
                  Detail: 'detail/:id',
                  Settings: 'settings',
                  ProfileDetail: 'home-profile/:userId',
                },
              },
              SearchTab: 'search',
              ProfileTab: {
                screens: {
                  ProfileHub: 'profile/:userId',
                  EditProfile: 'profile/edit',
                },
              },
            },
          },
          Notifications: 'notifications',
          About: 'about',
        },
      },
      NotFound: '*',
    },
  },
};

export const resolveNavigationState = (
  input: string,
): InitialState | undefined => {
  const rawState = getStateFromPath(normalizePath(input), linking.config);
  const state = rawState
    ? (JSON.parse(JSON.stringify(rawState)) as RouteState)
    : undefined;

  visitRoutes(state, route => {
    if (route.name !== 'Detail') {
      return;
    }

    const params = route.params as
      | { id: string; title?: string }
      | undefined;

    if (params?.id && !params.title) {
      route.params = {
        ...params,
        title: buildDetailTitle(params.id),
      };
    }
  });

  return state as InitialState | undefined;
};
