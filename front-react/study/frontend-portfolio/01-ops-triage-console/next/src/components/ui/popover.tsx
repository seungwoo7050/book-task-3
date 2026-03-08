"use client";

import {
  cloneElement,
  isValidElement,
  useEffect,
  useMemo,
  useRef,
  useState,
  type MouseEvent as ReactMouseEvent,
  type ReactElement,
  type ReactNode,
} from "react";

function mergeHandlers(
  original?: (event: ReactMouseEvent) => void,
  next?: (event: ReactMouseEvent) => void,
) {
  return (event: ReactMouseEvent) => {
    original?.(event);
    next?.(event);
  };
}

export function Popover({
  trigger,
  children,
}: {
  trigger: ReactNode;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const popoverId = useMemo(
    () => `popover-${Math.random().toString(36).slice(2, 8)}`,
    [],
  );

  useEffect(() => {
    function handlePointerDown(event: MouseEvent) {
      if (!containerRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handlePointerDown);
    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
    };
  }, []);

  const triggerNode = isValidElement(trigger)
    ? cloneElement(trigger as ReactElement<Record<string, unknown>>, {
        onClick: mergeHandlers(
          (trigger as ReactElement<Record<string, unknown>>).props.onClick as
            | ((event: ReactMouseEvent) => void)
            | undefined,
          () => setOpen((current) => !current),
        ),
        "aria-expanded": open,
        "aria-controls": popoverId,
        "aria-haspopup": "dialog",
      })
    : trigger;

  return (
    <div ref={containerRef} className="relative">
      {triggerNode}
      {open ? (
        <div
          id={popoverId}
          role="dialog"
          className="absolute right-0 top-[calc(100%+0.625rem)] z-50 w-80 rounded-2xl border border-slate-200 bg-white p-4 shadow-2xl"
        >
          {children}
        </div>
      ) : null}
    </div>
  );
}
