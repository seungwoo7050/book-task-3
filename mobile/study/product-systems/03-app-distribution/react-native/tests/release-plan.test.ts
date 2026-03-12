import { releaseTargets, summarizeReleaseTargets } from '../src/releasePlan';

describe('release plan', () => {
  it('defines the three release channels', () => {
    expect(releaseTargets.map(target => target.channel)).toEqual([
      'development',
      'staging',
      'production',
    ]);
  });

  it('builds stable rehearsal summary strings', () => {
    expect(summarizeReleaseTargets()[1]).toContain('rehearsal_staging');
    expect(summarizeReleaseTargets()[2]).toContain('production-summary.json');
  });
});
