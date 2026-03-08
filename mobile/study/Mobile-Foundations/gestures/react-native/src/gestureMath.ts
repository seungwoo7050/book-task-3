export function getSwipeDecision(
  translateX: number,
  threshold: number,
): 'like' | 'nope' | 'reset' {
  if (translateX >= threshold) {
    return 'like';
  }

  if (translateX <= -threshold) {
    return 'nope';
  }

  return 'reset';
}

export function getDismissProgress(translateY: number, maxDistance: number): number {
  const normalized = Math.min(Math.max(translateY / maxDistance, 0), 1);
  return Number(normalized.toFixed(2));
}

export function reorderByOffset<T>(
  items: T[],
  activeIndex: number,
  offsetY: number,
  rowHeight: number,
): T[] {
  const nextIndex = Math.min(
    items.length - 1,
    Math.max(0, activeIndex + Math.round(offsetY / rowHeight)),
  );

  if (nextIndex === activeIndex) {
    return items;
  }

  const draft = [...items];
  const [item] = draft.splice(activeIndex, 1);
  draft.splice(nextIndex, 0, item);
  return draft;
}
