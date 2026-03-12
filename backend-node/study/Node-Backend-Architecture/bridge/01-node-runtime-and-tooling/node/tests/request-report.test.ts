import path from "node:path";

import { describe, expect, it, vi } from "vitest";

import { runCli } from "../src/cli";
import { formatSummary, readRequestLog, summarizeRequests } from "../src/request-report";

const fixturePath = path.resolve(__dirname, "../../problem/data/request-log.ndjson");

describe("request report", () => {
  it("reads NDJSON records from disk", async () => {
    const records = await readRequestLog(fixturePath);

    expect(records).toHaveLength(5);
    expect(records[0]?.route).toBe("/books");
  });

  it("builds a summary from records", async () => {
    const records = await readRequestLog(fixturePath);
    const summary = summarizeRequests(fixturePath, records);

    expect(summary.totalRequests).toBe(5);
    expect(summary.uniqueUsers).toBe(3);
    expect(summary.errorCount).toBe(2);
    expect(summary.perRoute["/books"]).toBe(3);
  });

  it("formats a text report", async () => {
    const records = await readRequestLog(fixturePath);
    const summary = summarizeRequests(fixturePath, records);
    const output = formatSummary(summary, "text");

    expect(output).toContain("Total requests: 5");
    expect(output).toContain("- /books: 3");
  });
});

describe("cli", () => {
  it("prints json when REPORT_FORMAT=json", async () => {
    const stdout = { write: vi.fn() };
    const stderr = { write: vi.fn() };

    const exitCode = await runCli([fixturePath], { REPORT_FORMAT: "json" }, stdout, stderr);

    expect(exitCode).toBe(0);
    expect(stdout.write).toHaveBeenCalledOnce();
    expect(stdout.write.mock.calls[0]?.[0]).toContain("\"totalRequests\": 5");
    expect(stderr.write).not.toHaveBeenCalled();
  });

  it("returns a non-zero exit code for invalid formats", async () => {
    const stdout = { write: vi.fn() };
    const stderr = { write: vi.fn() };

    const exitCode = await runCli([fixturePath], { REPORT_FORMAT: "yaml" }, stdout, stderr);

    expect(exitCode).toBe(1);
    expect(stderr.write).toHaveBeenCalledWith("REPORT_FORMAT must be either text or json\n");
  });
});
