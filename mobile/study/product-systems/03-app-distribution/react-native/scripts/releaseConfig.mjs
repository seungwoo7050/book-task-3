import fs from 'node:fs';
import path from 'node:path';

export const projectRoot = path.resolve(new URL('..', import.meta.url).pathname);

export function parseEnvFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const entries = content
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0 && !line.startsWith('#'))
    .map(line => {
      const separator = line.indexOf('=');
      return [line.slice(0, separator), line.slice(separator + 1)];
    });
  return Object.fromEntries(entries);
}

export function getEnvExamples() {
  const examples = [
    '.env.development.example',
    '.env.staging.example',
    '.env.production.example',
  ];

  return examples.map(name => {
    const filePath = path.join(projectRoot, name);
    return {
      name,
      filePath,
      values: parseEnvFile(filePath),
    };
  });
}

export function buildValidationSummary() {
  const envExamples = getEnvExamples();
  const baselineKeys = Object.keys(envExamples[0].values);
  const envChecks = envExamples.map(example => ({
    name: example.name,
    keys: Object.keys(example.values),
    values: example.values,
  }));

  return {
    checkedAt: '2026-03-08',
    envChecks,
    consistentKeys: envChecks.every(
      check => JSON.stringify(check.keys) === JSON.stringify(baselineKeys),
    ),
    workflowPresent: fs.existsSync(
      path.join(projectRoot, '.github', 'workflows', 'mobile-release.yml'),
    ),
    fastlanePresent: fs.existsSync(path.join(projectRoot, 'fastlane', 'Fastfile')),
  };
}
