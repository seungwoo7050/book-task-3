export const MODULE_SPECS = [
  {
    name: 'BatteryModule',
    methods: ['getBatteryLevel', 'getChargingStatus', 'subscribe'],
  },
  {
    name: 'HapticsModule',
    methods: ['vibrate', 'impactFeedback', 'notificationFeedback'],
  },
  {
    name: 'SensorModule',
    methods: ['startAccelerometer', 'stopAccelerometer', 'startGyroscope', 'stopGyroscope'],
  },
] as const;

export function buildGeneratedSummary() {
  return MODULE_SPECS.map(spec => ({
    module: spec.name,
    methodCount: spec.methods.length,
  }));
}
