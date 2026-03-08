import React from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { fireEvent, render, screen, waitFor } from '@testing-library/react-native';

import App from '../App';

function jsonResponse(body: unknown, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    text: () => Promise.resolve(JSON.stringify(body)),
  });
}

describe('incident ops app shell', () => {
  beforeEach(async () => {
    await AsyncStorage.clear();
    (global.fetch as jest.Mock).mockImplementation((input: string, init?: RequestInit) => {
      if (input.endsWith('/auth/login')) {
        return jsonResponse({
          token: 'token-1',
          actor: {
            userId: 'reporter.demo',
            role: 'REPORTER',
          },
        });
      }

      if (input.includes('/incidents?')) {
        return jsonResponse({
          incidents: [
            {
              id: 'inc-1',
              title: 'Database latency spike',
              description: 'P1 impact on checkout queries',
              severity: 'P1',
              status: 'OPEN',
              createdBy: 'reporter.demo',
              approvalId: null,
              createdAt: '2026-03-07T00:00:00.000Z',
              updatedAt: '2026-03-07T00:00:00.000Z',
            },
          ],
          nextCursor: null,
        });
      }

      if (input.endsWith('/incidents') && init?.method === 'POST') {
        return jsonResponse({
          incident: {
            id: 'inc-2',
            title: 'Queued follow-up incident',
            description: 'created in app shell test',
            severity: 'P2',
            status: 'OPEN',
            createdBy: 'reporter.demo',
            approvalId: null,
            createdAt: '2026-03-07T00:05:00.000Z',
            updatedAt: '2026-03-07T00:05:00.000Z',
          },
          eventId: 2,
        }, 201);
      }

      if (input.includes('/audit?incidentId=')) {
        return jsonResponse({
          items: [],
        });
      }

      throw new Error(`unexpected fetch ${input}`);
    });
  });

  afterEach(() => {
    (global.fetch as jest.Mock).mockReset();
  });

  it('logs in and opens the incident feed', async () => {
    render(<App />);

    fireEvent.changeText(
      await screen.findByTestId('login-user-id-input'),
      'reporter.demo',
    );
    fireEvent.press(screen.getByTestId('login-submit-button'));

    expect(await screen.findByText('Database latency spike')).toBeTruthy();
    expect(screen.getByTestId('new-incident-button')).toBeTruthy();
  });

  it('queues a new incident from the create screen', async () => {
    render(<App />);

    fireEvent.changeText(
      await screen.findByTestId('login-user-id-input'),
      'reporter.demo',
    );
    fireEvent.press(screen.getByTestId('login-submit-button'));

    fireEvent.press(await screen.findByTestId('new-incident-button'));
    fireEvent.changeText(
      await screen.findByTestId('create-title-input'),
      'Queued follow-up incident',
    );
    fireEvent.press(screen.getByTestId('queue-incident-button'));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/incidents'),
        expect.objectContaining({
          method: 'POST',
        }),
      );
    });
  });
});
