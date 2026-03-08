import { describe, expect, it } from "vitest";
import {
  createRetryableError,
  shouldSimulateFailure,
  waitForLatency,
} from "@/lib/simulate";

describe("service simulation helpers", () => {
  it("ignores failure rate in stable mode", () => {
    expect(
      shouldSimulateFailure(
        {
          latencyMs: 0,
          failureRate: 1,
          failNextRequest: false,
          mode: "stable",
        },
        0,
      ),
    ).toBe(false);
  });

  it("fails immediately when failNextRequest is set", () => {
    expect(
      shouldSimulateFailure(
        {
          latencyMs: 0,
          failureRate: 0,
          failNextRequest: true,
          mode: "stable",
        },
        0.99,
      ),
    ).toBe(true);
  });

  it("uses the provided random value in chaos mode", () => {
    expect(
      shouldSimulateFailure(
        {
          latencyMs: 0,
          failureRate: 0.35,
          failNextRequest: false,
          mode: "chaos",
        },
        0.2,
      ),
    ).toBe(true);
    expect(
      shouldSimulateFailure(
        {
          latencyMs: 0,
          failureRate: 0.35,
          failNextRequest: false,
          mode: "chaos",
        },
        0.8,
      ),
    ).toBe(false);
  });

  it("creates a retryable service error", () => {
    const error = createRetryableError();

    expect(error.code).toBe("DEMO_TRANSIENT_FAILURE");
    expect(error.retryable).toBe(true);
  });

  it("resolves immediately for non-positive latency", async () => {
    await expect(waitForLatency(0)).resolves.toBeUndefined();
  });
});
