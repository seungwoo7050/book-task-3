import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function Toast({
  tone,
  title,
  description,
  actionLabel,
  onAction,
  onDismiss,
}: {
  tone: "success" | "error";
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  onDismiss: () => void;
}) {
  return (
    <div
      className={cn(
        "fixed bottom-4 right-4 z-50 w-[min(420px,calc(100vw-2rem))] rounded-2xl border px-4 py-4 shadow-2xl",
        tone === "success"
          ? "border-emerald-200 bg-emerald-50"
          : "border-red-200 bg-red-50",
      )}
      role="status"
      aria-live="polite"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-1">
          <p className="text-sm font-semibold text-slate-950">{title}</p>
          <p className="text-sm text-slate-700">{description}</p>
        </div>
        <button
          type="button"
          className="rounded-full px-2 py-1 text-xs text-slate-600 hover:bg-white"
          onClick={onDismiss}
        >
          Close
        </button>
      </div>
      {(actionLabel || onAction) && onAction ? (
        <div className="mt-3">
          <Button size="sm" variant={tone === "success" ? "primary" : "danger"} onClick={onAction}>
            {actionLabel}
          </Button>
        </div>
      ) : null}
    </div>
  );
}

