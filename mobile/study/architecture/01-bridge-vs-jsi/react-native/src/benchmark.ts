export interface BenchmarkRun {
  label: string;
  payloadSize: number;
  samples: number[];
}

export interface BenchmarkStats {
  label: string;
  payloadSize: number;
  mean: number;
  stddev: number;
}

export const RUNS: BenchmarkRun[] = [
  {
    label: 'async serialized',
    payloadSize: 1000,
    samples: [42, 45, 44, 47, 43],
  },
  {
    label: 'sync direct-call',
    payloadSize: 1000,
    samples: [11, 10, 12, 10, 11],
  },
];

export function computeStats(run: BenchmarkRun): BenchmarkStats {
  const mean = run.samples.reduce((sum, value) => sum + value, 0) / run.samples.length;
  const variance =
    run.samples.reduce((sum, value) => sum + (value - mean) ** 2, 0) / run.samples.length;

  return {
    label: run.label,
    payloadSize: run.payloadSize,
    mean: Number(mean.toFixed(2)),
    stddev: Number(Math.sqrt(variance).toFixed(2)),
  };
}

export function buildExport() {
  return {
    generatedAt: '2026-03-08',
    results: RUNS.map(computeStats),
  };
}
