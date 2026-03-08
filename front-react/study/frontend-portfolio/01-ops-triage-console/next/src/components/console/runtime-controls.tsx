"use client";

import { Button } from "@/components/ui/button";
import { Popover } from "@/components/ui/popover";
import { Select } from "@/components/ui/select";
import { Tooltip } from "@/components/ui/tooltip";
import { Badge } from "@/components/ui/badge";
import { type DemoRuntimeConfig } from "@/lib/types";

const latencyOptions = [
  { value: "0", label: "0 ms" },
  { value: "220", label: "220 ms" },
  { value: "800", label: "800 ms" },
];

const modeOptions = [
  { value: "stable", label: "Stable" },
  { value: "chaos", label: "Chaos" },
];

export function RuntimeControls({
  runtime,
  setRuntime,
  onResetDemo,
  isResetPending,
}: {
  runtime: DemoRuntimeConfig;
  setRuntime: (nextValue: DemoRuntimeConfig) => void;
  onResetDemo: () => void;
  isResetPending: boolean;
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <Tooltip content="Local-first async service with latency and retryable error simulation.">
        <Badge tone={runtime.mode === "chaos" ? "warning" : "ink"}>
          {runtime.mode === "chaos" ? "Chaos mode" : "Stable mode"}
        </Badge>
      </Tooltip>
      <Tooltip content="Latency is applied to every async service call.">
        <Badge tone="neutral">{runtime.latencyMs} ms</Badge>
      </Tooltip>
      <Popover
        trigger={
          <Button variant="secondary" size="sm" aria-label="Open demo controls">
            Demo controls
          </Button>
        }
      >
        <div className="space-y-4">
          <div>
            <p className="text-sm font-semibold text-slate-950">Demo runtime</p>
            <p className="mt-1 text-sm text-slate-600">
              Tune latency, switch error mode, or inject a one-off write failure.
            </p>
          </div>
          <div className="space-y-3">
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                Mode
              </label>
              <Select
                ariaLabel="Demo mode"
                value={runtime.mode}
                onValueChange={(value) =>
                  setRuntime({
                    ...runtime,
                    mode: value as DemoRuntimeConfig["mode"],
                    failureRate: value === "chaos" ? 0.35 : 0,
                    failNextRequest: false,
                  })
                }
                placeholder="Select mode"
                options={modeOptions}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                Latency
              </label>
              <Select
                ariaLabel="Demo latency"
                value={String(runtime.latencyMs)}
                onValueChange={(value) =>
                  setRuntime({
                    ...runtime,
                    latencyMs: Number(value),
                  })
                }
                placeholder="Select latency"
                options={latencyOptions}
              />
            </div>
          </div>
          <div className="grid gap-2 sm:grid-cols-2">
            <Button
              variant="subtle"
              size="sm"
              onClick={() =>
                setRuntime({
                  latencyMs: 220,
                  mode: "stable",
                  failureRate: 0,
                  failNextRequest: false,
                })
              }
            >
              Stable preset
            </Button>
            <Button
              variant="subtle"
              size="sm"
              onClick={() =>
                setRuntime({
                  latencyMs: 800,
                  mode: "chaos",
                  failureRate: 0.35,
                  failNextRequest: false,
                })
              }
            >
              Chaos preset
            </Button>
            <Button
              variant="danger"
              size="sm"
              data-testid="fail-next-request"
              onClick={() =>
                setRuntime({
                  ...runtime,
                  failNextRequest: true,
                })
              }
            >
              Fail next request
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={onResetDemo}
              disabled={isResetPending}
            >
              {isResetPending ? "Resetting..." : "Reset demo data"}
            </Button>
          </div>
        </div>
      </Popover>
    </div>
  );
}
