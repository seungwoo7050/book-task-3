import React from 'react';
import { fireEvent, render, screen } from '@testing-library/react-native';
import App from '../App';
import {
  acknowledgeIncident,
  decideApproval,
  initialApproval,
  initialIncident,
  loginAs,
  replayFrom,
  requestResolution,
} from '../src/harnessModel';

describe('incident ops harness model', () => {
  it('acknowledges an open incident for an operator', () => {
    expect(acknowledgeIncident(initialIncident, loginAs('OPERATOR')).incident.status).toBe('ACKED');
  });

  it('requests and approves resolution', () => {
    const requested = requestResolution(
      { ...initialIncident, status: 'ACKED' },
      loginAs('OPERATOR'),
    );
    const approved = decideApproval(
      requested.incident,
      requested.approval ?? initialApproval,
      loginAs('APPROVER'),
      'APPROVE',
    );
    expect(approved.incident.status).toBe('RESOLVED');
    expect(approved.approval.status).toBe('APPROVED');
  });

  it('replays only missed events', () => {
    expect(replayFrom(2)).toHaveLength(2);
  });
});

describe('incident ops harness app', () => {
  it('lets an operator ack and request resolution', () => {
    render(<App />);

    fireEvent.press(screen.getByTestId('role-button-OPERATOR'));
    fireEvent.press(screen.getByTestId('ack-button'));
    expect(screen.getByText(/status: ACKED/)).toBeTruthy();

    fireEvent.press(screen.getByTestId('request-resolution-button'));
    expect(screen.getByText(/status: RESOLUTION_PENDING/)).toBeTruthy();
  });

  it('lets an approver approve after resolution is requested', () => {
    render(<App />);

    fireEvent.press(screen.getByTestId('role-button-OPERATOR'));
    fireEvent.press(screen.getByTestId('ack-button'));
    fireEvent.press(screen.getByTestId('request-resolution-button'));
    fireEvent.press(screen.getByTestId('role-button-APPROVER'));
    fireEvent.press(screen.getByTestId('approve-button'));

    expect(screen.getByText(/status: RESOLVED/)).toBeTruthy();
    expect(screen.getByText('APPROVED')).toBeTruthy();
  });
});
