import { getDismissProgress, getSwipeDecision, reorderByOffset } from '../src/gestureMath';

describe('gesture math helpers', () => {
  it('calculates swipe decisions from threshold', () => {
    expect(getSwipeDecision(180, 120)).toBe('like');
    expect(getSwipeDecision(-180, 120)).toBe('nope');
    expect(getSwipeDecision(40, 120)).toBe('reset');
  });

  it('reorders a list when offset crosses a row', () => {
    expect(reorderByOffset(['a', 'b', 'c'], 0, 58, 58)).toEqual(['b', 'a', 'c']);
    expect(reorderByOffset(['a', 'b', 'c'], 2, -58, 58)).toEqual(['a', 'c', 'b']);
  });

  it('clamps dismiss progress', () => {
    expect(getDismissProgress(0, 160)).toBe(0);
    expect(getDismissProgress(80, 160)).toBe(0.5);
    expect(getDismissProgress(300, 160)).toBe(1);
  });
});
