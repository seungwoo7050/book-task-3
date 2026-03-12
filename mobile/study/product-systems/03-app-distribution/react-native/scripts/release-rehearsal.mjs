import fs from 'node:fs';
import path from 'node:path';
import { buildValidationSummary, projectRoot } from './releaseConfig.mjs';

const releaseDir = path.join(projectRoot, 'release');
fs.mkdirSync(releaseDir, { recursive: true });

const summary = {
  ...buildValidationSummary(),
  rehearsal: {
    android: 'signed build rehearsal configured via Fastlane lane and placeholder keystore env keys',
    ios: 'archive dry-run configured via Fastlane lane and placeholder export options',
    workflow: 'mobile-release.yml runs typecheck, test, release:validate',
  },
};

if (!summary.consistentKeys || !summary.workflowPresent || !summary.fastlanePresent) {
  console.error('release rehearsal prerequisites failed');
  process.exit(1);
}

const outputPath = path.join(releaseDir, 'rehearsal-summary.json');
fs.writeFileSync(outputPath, `${JSON.stringify(summary, null, 2)}\n`);
console.log(`release rehearsal summary written to ${outputPath}`);
