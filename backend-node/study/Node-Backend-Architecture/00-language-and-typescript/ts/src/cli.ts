import {
  formatBookCard,
  toNormalizedBook,
  type BookDraft,
} from "./catalog";

type WriteTarget = {
  write(chunk: string): void;
};

function readFlag(args: string[], name: string): string | undefined {
  const index = args.indexOf(name);
  if (index < 0) {
    return undefined;
  }

  return args[index + 1];
}

export function parseArgs(args: string[]): BookDraft {
  const title = readFlag(args, "--title");
  const author = readFlag(args, "--author");
  const yearValue = readFlag(args, "--year");
  const tagsValue = readFlag(args, "--tags");
  const description = readFlag(args, "--description");

  if (!title || !author || !yearValue || !tagsValue) {
    throw new Error("Required flags: --title --author --year --tags");
  }

  const publishedYear = Number(yearValue);
  if (!Number.isInteger(publishedYear) || publishedYear < 0) {
    throw new Error("--year must be a positive integer");
  }

  return {
    title,
    author,
    publishedYear,
    tags: tagsValue.split(","),
    description,
  };
}

export function runCli(args: string[], stdout: WriteTarget, stderr: WriteTarget): number {
  try {
    const draft = parseArgs(args);
    const normalized = toNormalizedBook(draft);
    stdout.write(`${formatBookCard(normalized)}\n`);

    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown CLI error";
    stderr.write(`${message}\n`);

    return 1;
  }
}

if (require.main === module) {
  process.exitCode = runCli(process.argv.slice(2), process.stdout, process.stderr);
}
