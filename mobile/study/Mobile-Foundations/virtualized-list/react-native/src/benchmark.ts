export interface BenchmarkMetric {
  fps: number;
  initialRenderMs: number;
  blankAreaMs: number;
  peakMemoryMb: number;
  mountCount: number;
}

export interface BenchmarkSummary {
  fpsGain: number;
  renderGainMs: number;
  blankAreaGainMs: number;
  memoryGainMb: number;
  mountSavings: number;
}

export const SAMPLE_BENCHMARK = {
  flatList: {
    fps: 47,
    initialRenderMs: 222,
    blankAreaMs: 61,
    peakMemoryMb: 188,
    mountCount: 1230,
  },
  flashList: {
    fps: 58,
    initialRenderMs: 141,
    blankAreaMs: 18,
    peakMemoryMb: 134,
    mountCount: 472,
  },
} satisfies Record<string, BenchmarkMetric>;

export function computeBenchmarkSummary(
  flatList: BenchmarkMetric,
  flashList: BenchmarkMetric,
): BenchmarkSummary {
  return {
    fpsGain: flashList.fps - flatList.fps,
    renderGainMs: flatList.initialRenderMs - flashList.initialRenderMs,
    blankAreaGainMs: flatList.blankAreaMs - flashList.blankAreaMs,
    memoryGainMb: flatList.peakMemoryMb - flashList.peakMemoryMb,
    mountSavings: flatList.mountCount - flashList.mountCount,
  };
}
