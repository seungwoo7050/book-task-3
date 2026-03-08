"use client";

import {
  useEffect,
  useState,
  type MouseEvent,
  type ReactNode,
} from "react";
import { createPortal } from "react-dom";

export function Dialog({
  open,
  onOpenChange,
  title,
  children,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  children: ReactNode;
}) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!open) {
      return;
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onOpenChange(false);
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [open, onOpenChange]);

  if (!mounted || !open) {
    return null;
  }

  function stopPropagation(event: MouseEvent<HTMLDivElement>) {
    event.stopPropagation();
  }

  return createPortal(
    <div className="fixed inset-0 z-50" role="presentation" onClick={() => onOpenChange(false)}>
      <div className="absolute inset-0 bg-slate-950/30 backdrop-blur-[2px]" />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="absolute inset-x-4 top-6 max-h-[90vh] overflow-y-auto rounded-3xl bg-white p-5 shadow-2xl sm:left-1/2 sm:w-[720px] sm:-translate-x-1/2"
        onClick={stopPropagation}
      >
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
          <button
            type="button"
            aria-label="Close dialog"
            className="rounded-full p-2 text-slate-500 hover:bg-slate-100"
            onClick={() => onOpenChange(false)}
          >
            <span aria-hidden="true" className="text-lg leading-none">
              x
            </span>
          </button>
        </div>
        {children}
      </div>
    </div>,
    document.body,
  );
}
