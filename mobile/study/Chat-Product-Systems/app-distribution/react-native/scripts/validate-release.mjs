import { buildValidationSummary } from './releaseConfig.mjs';

const summary = buildValidationSummary();

if (!summary.consistentKeys) {
  console.error('env example keys are not aligned');
  process.exit(1);
}

if (!summary.workflowPresent || !summary.fastlanePresent) {
  console.error('required release assets are missing');
  process.exit(1);
}

console.log(JSON.stringify(summary, null, 2));
