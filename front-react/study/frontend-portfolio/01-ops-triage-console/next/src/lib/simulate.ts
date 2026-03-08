import { type DemoRuntimeConfig, type DemoServiceError } from "@/lib/types";

export async function waitForLatency(latencyMs: number): Promise<void> {
  if (latencyMs <= 0) {
    return;
  }

  await new Promise((resolve) => {
    setTimeout(resolve, latencyMs);
  });
}

export function createRetryableError(): DemoServiceError {
  const error = new Error("Transient failure. Retry the request.") as DemoServiceError;
  error.code = "DEMO_TRANSIENT_FAILURE";
  error.retryable = true;
  return error;
}

export function shouldSimulateFailure(
  config: DemoRuntimeConfig,
  randomValue = Math.random(),
): boolean {
  if (config.failNextRequest) {
    return true;
  }

  if (config.mode === "stable") {
    return false;
  }

  return randomValue < config.failureRate;
}

