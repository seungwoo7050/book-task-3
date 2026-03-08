import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react-native';

import { resolveNavigationState } from '../src/navigation/linking';
import {
  DetailScreen,
  HomeScreen,
  NotFoundScreen,
  SettingsScreen,
} from '../src/screens/AppScreens';

describe('navigation pilot', () => {
  it('renders the stack screens and emits typed navigation calls', () => {
    const homeNavigate = jest.fn();
    const detailNavigate = jest.fn();
    const settingsNavigate = jest.fn();
    const goHome = jest.fn();

    render(
      <HomeScreen
        navigation={
          {
            getParent: () => ({
              getParent: () => ({
                dispatch: jest.fn(),
              }),
            }),
            navigate: homeNavigate,
          } as never
        }
        route={{ key: 'home', name: 'Home' }}
      />,
    );

    expect(screen.getByRole('header', { name: 'Home screen' })).toBeTruthy();

    fireEvent.press(screen.getByText('Open detail example'));

    expect(homeNavigate).toHaveBeenCalledWith('Detail', {
      id: 'abc123',
      title: 'On-call deep link drill',
    });

    render(
      <DetailScreen
        navigation={{ navigate: detailNavigate } as never}
        route={{
          key: 'detail',
          name: 'Detail',
          params: {
            id: 'abc123',
            title: 'On-call deep link drill',
          },
        }}
      />,
    );

    expect(screen.getByText('id: abc123')).toBeTruthy();
    fireEvent.press(screen.getByText('Continue to settings'));
    expect(detailNavigate).toHaveBeenCalledWith('Settings');

    render(
      <SettingsScreen
        navigation={{ navigate: settingsNavigate } as never}
        route={{ key: 'settings', name: 'Settings' }}
      />,
    );

    fireEvent.press(screen.getByText('Open profile detail'));
    expect(settingsNavigate).toHaveBeenCalledWith('ProfileDetail', {
      userId: 'operator-24',
    });

    render(
      <NotFoundScreen
        navigation={{ navigate: goHome } as never}
        route={{ key: 'missing', name: 'NotFound' }}
      />,
    );

    expect(screen.getByRole('header', { name: 'Not found' })).toBeTruthy();
    fireEvent.press(screen.getByText('Go home'));
    expect(goHome).toHaveBeenCalledWith('Drawer', {
      params: {
        params: { screen: 'Home' },
        screen: 'HomeTab',
      },
      screen: 'Main',
    });
  });

  it('maps known deep links into nested navigation state', () => {
    const detailState = resolveNavigationState('myapp://detail/abc123');
    const profileState = resolveNavigationState(
      'https://myapp.example.com/profile/user42',
    );

    expect(JSON.stringify(detailState)).toContain('"name":"Detail"');
    expect(JSON.stringify(detailState)).toContain('"id":"abc123"');
    expect(JSON.stringify(detailState)).toContain(
      '"title":"Detail route for abc123"',
    );

    expect(JSON.stringify(profileState)).toContain('"name":"ProfileHub"');
    expect(JSON.stringify(profileState)).toContain('"userId":"user42"');
  });

  it('routes unknown paths to the fallback state', () => {
    const notFoundState = resolveNavigationState('myapp://unknown/path');

    expect(JSON.stringify(notFoundState)).toContain('"name":"NotFound"');
  });
});
