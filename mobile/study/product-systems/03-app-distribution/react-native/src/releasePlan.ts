export type ReleaseChannel = 'development' | 'staging' | 'production';

export interface ReleaseTarget {
  channel: ReleaseChannel;
  iosLane: string;
  androidLane: string;
  artifact: string;
}

export const releaseTargets: ReleaseTarget[] = [
  {
    channel: 'development',
    iosLane: 'ios validate_env',
    androidLane: 'android validate_env',
    artifact: 'release/development-summary.json',
  },
  {
    channel: 'staging',
    iosLane: 'ios rehearsal_staging',
    androidLane: 'android rehearsal_staging',
    artifact: 'release/staging-summary.json',
  },
  {
    channel: 'production',
    iosLane: 'ios rehearsal_production',
    androidLane: 'android rehearsal_production',
    artifact: 'release/production-summary.json',
  },
];

export function summarizeReleaseTargets(): string[] {
  return releaseTargets.map(
    target =>
      `${target.channel}: ${target.iosLane} | ${target.androidLane} -> ${target.artifact}`,
  );
}
