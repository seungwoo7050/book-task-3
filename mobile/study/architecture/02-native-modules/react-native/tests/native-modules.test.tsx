import { MODULE_SPECS, buildGeneratedSummary } from '../src/specs';

describe('native modules specs', () => {
  it('defines three module specs', () => {
    expect(MODULE_SPECS).toHaveLength(3);
    expect(MODULE_SPECS[0].methods.length).toBeGreaterThan(0);
  });

  it('builds codegen summary', () => {
    expect(buildGeneratedSummary()).toEqual([
      { module: 'BatteryModule', methodCount: 3 },
      { module: 'HapticsModule', methodCount: 3 },
      { module: 'SensorModule', methodCount: 4 },
    ]);
  });
});
