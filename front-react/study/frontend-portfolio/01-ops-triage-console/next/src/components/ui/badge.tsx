import { type HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

const toneMap = {
  neutral: "bg-slate-100 text-slate-700",
  warning: "bg-amber-100 text-amber-800",
  danger: "bg-red-100 text-red-700",
  success: "bg-emerald-100 text-emerald-700",
  ink: "bg-slate-900 text-white",
};

export function Badge({
  className,
  tone = "neutral",
  ...props
}: HTMLAttributes<HTMLSpanElement> & {
  tone?: keyof typeof toneMap;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-semibold tracking-[0.02em]",
        toneMap[tone],
        className,
      )}
      {...props}
    />
  );
}

