"use client";

import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import { cn } from "@/lib/utils";

export function Checkbox({
  className,
  ...props
}: CheckboxPrimitive.CheckboxProps & {
  className?: string;
}) {
  return (
    <CheckboxPrimitive.Root
      className={cn(
        "inline-flex h-4 w-4 items-center justify-center rounded border border-slate-400 bg-white text-slate-950 outline-none transition focus-visible:ring-2 focus-visible:ring-slate-400",
        className,
      )}
      {...props}
    >
      <CheckboxPrimitive.Indicator>
        <svg
          aria-hidden="true"
          viewBox="0 0 16 16"
          className="h-3.5 w-3.5"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M3.5 8.5 6.5 11.5 12.5 4.5" />
        </svg>
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  );
}
