import fs from 'node:fs';
import path from 'node:path';

const outputDir = path.join(process.cwd(), 'generated');
fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(
  path.join(outputDir, 'modules.json'),
  JSON.stringify(
    [
      { module: 'BatteryModule', methodCount: 3 },
      { module: 'HapticsModule', methodCount: 3 },
      { module: 'SensorModule', methodCount: 4 },
    ],
    null,
    2,
  ),
);
console.log('generated summary written to generated/modules.json');
