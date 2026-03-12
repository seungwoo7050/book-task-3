import React from 'react';
import { render } from '@testing-library/react-native';
import App from '../App';
import {
  SAMPLE_BENCHMARK,
  computeBenchmarkSummary,
} from '../src/benchmark';
import { createDeterministicItems, itemHeightForType } from '../src/listData';
import {
  createPaginationState,
  isPaginationComplete,
  loadNextPage,
} from '../src/pagination';

describe('virtualized list study', () => {
  it('renders the shell', () => {
    const screen = render(<App />);
    expect(screen.getByText('Virtualized List Performance')).toBeTruthy();
    expect(screen.getByText('FlatList')).toBeTruthy();
    expect(screen.getByText('FlashList v2')).toBeTruthy();
  });

  it('creates deterministic items', () => {
    const first = createDeterministicItems(24, 3);
    const second = createDeterministicItems(24, 3);
    expect(first).toEqual(second);
    expect(itemHeightForType(first[0].type)).toBeGreaterThan(0);
  });

  it('advances pagination until complete', () => {
    const initial = createPaginationState(130, 50);
    const next = loadNextPage(initial);
    const final = loadNextPage(loadNextPage(next));
    expect(next.cursor).toBe(100);
    expect(final.cursor).toBe(130);
    expect(isPaginationComplete(final)).toBe(true);
  });

  it('computes benchmark summary deltas', () => {
    const summary = computeBenchmarkSummary(
      SAMPLE_BENCHMARK.flatList,
      SAMPLE_BENCHMARK.flashList,
    );
    expect(summary.fpsGain).toBeGreaterThan(0);
    expect(summary.mountSavings).toBeGreaterThan(0);
  });
});
