import { RUNS, buildExport, computeStats } from '../src/benchmark';

describe('bridge vs jsi benchmark helpers', () => {
  it('computes statistics for each run', () => {
    const stats = computeStats(RUNS[0]);
    expect(stats.mean).toBeGreaterThan(stats.stddev);
  });

  it('builds deterministic export json', () => {
    expect(buildExport()).toEqual({
      generatedAt: '2026-03-08',
      results: RUNS.map(computeStats),
    });
  });
});
