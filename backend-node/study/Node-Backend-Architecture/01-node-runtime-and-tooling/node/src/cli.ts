import {
  formatSummary,
  readRequestLog,
  summarizeRequests,
} from "./request-report";

type WriteTarget = {
  write(chunk: string): void;
};

type EnvLike = Record<string, string | undefined>;

export async function runCli(
  args: string[],
  env: EnvLike,
  stdout: WriteTarget,
  stderr: WriteTarget,
): Promise<number> {
  const filePath = args[0];
  if (!filePath) {
    stderr.write("Usage: pnpm start -- <path-to-ndjson>\n");

    return 1;
  }

  const requestedFormat = env.REPORT_FORMAT ?? "text";
  if (requestedFormat !== "text" && requestedFormat !== "json") {
    stderr.write("REPORT_FORMAT must be either text or json\n");

    return 1;
  }

  try {
    const records = await readRequestLog(filePath);
    const summary = summarizeRequests(filePath, records);
    stdout.write(`${formatSummary(summary, requestedFormat)}\n`);

    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown CLI error";
    stderr.write(`${message}\n`);

    return 1;
  }
}

if (require.main === module) {
  runCli(process.argv.slice(2), process.env, process.stdout, process.stderr)
    .then((exitCode) => {
      process.exitCode = exitCode;
    });
}
