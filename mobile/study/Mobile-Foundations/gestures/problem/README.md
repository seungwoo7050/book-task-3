# Problem: Fluid Animations

> Status: PARTIAL
> Scope: 문제 정의 문서
> Last Checked: 2026-03-02


## Problem Statement

Build three animation-heavy features that demonstrate mastery of **Reanimated 3** and **Gesture Handler**. Each feature must run entirely on the UI thread with no JS thread involvement during the animation.

---

## Part 1: Tinder Swipe Card

### Requirements

Implement a card stack where the user can swipe cards left (reject) or right (like):

1. **Pan gesture** — Card follows finger position during drag
2. **Rotation** — Card rotates proportionally to horizontal displacement
3. **Opacity indicators** — "LIKE" / "NOPE" labels fade in based on swipe direction
4. **Snap decision** — If swipe exceeds threshold → animate card off-screen; otherwise → spring back to center
5. **Card stack** — Next card is visible beneath the current card (scaled down slightly)
6. **Spring physics** — The return-to-center animation uses spring dynamics

### Visual Specification

```
                    ┌──────────────────┐
        NOPE ← ←   │                  │   → → LIKE
                    │   Card Content   │
                    │   (Image + Name) │
                    │                  │
                    └──────────────────┘
                          ↕ drag

  Swipe left threshold: -120px → animate off-screen left
  Swipe right threshold: +120px → animate off-screen right
  Below threshold: spring back to center
```

### Animation Properties

| Property | Behavior |
|----------|----------|
| `translateX` | Follows horizontal pan gesture |
| `translateY` | Follows vertical pan gesture (limited range) |
| `rotate` | `translateX / 10` degrees |
| `opacity (LIKE)` | `translateX / 120` (0 to 1, clamped) |
| `opacity (NOPE)` | `-translateX / 120` (0 to 1, clamped) |
| `scale (next card)` | Interpolates from 0.9 to 1.0 as top card is swiped |

### Snap Behavior

```typescript
// On gesture end:
if (Math.abs(translateX.value) > SWIPE_THRESHOLD) {
  // Fling card off screen
  translateX.value = withTiming(direction * SCREEN_WIDTH, { duration: 300 });
  // Trigger callback
  runOnJS(onSwipe)(direction > 0 ? 'like' : 'nope');
} else {
  // Spring back to center
  translateX.value = withSpring(0, { damping: 15, stiffness: 150 });
  translateY.value = withSpring(0, { damping: 15, stiffness: 150 });
}
```

---

## Part 2: Drag-to-Reorder List

### Requirements

Implement a vertical list where items can be long-pressed and dragged to reorder:

1. **Long press activation** — Item becomes draggable only after a 200ms long press
2. **Visual feedback** — Dragged item scales up (1.05x) and has an elevated shadow
3. **Auto-scroll** — List scrolls when dragged item approaches the top/bottom edge
4. **Position swap** — Other items animate smoothly to fill/make space
5. **Drop animation** — Item springs into its final position on release
6. **Haptic feedback** — Trigger a haptic pulse on pickup and on each position swap

### Visual Specification

```
  ┌────────────────────────┐
  │  Item A                │
  ├────────────────────────┤
  │  Item B                │  ← long press → lift
  ├────────────────────────┤       │
  │  Item C                │       ↓ drag down
  ├────────────────────────┤
  │  Item D                │
  └────────────────────────┘

  After drag:
  ┌────────────────────────┐
  │  Item A                │
  ├────────────────────────┤
  │  Item C                │  ← moved up
  ├────────────────────────┤
  │  Item B                │  ← dropped here
  ├────────────────────────┤
  │  Item D                │
  └────────────────────────┘
```

### Gesture Composition

```typescript
const longPress = Gesture.LongPress()
  .minDuration(200)
  .onStart(() => {
    'worklet';
    isActive.value = true;
    runOnJS(triggerHaptic)();
  });

const pan = Gesture.Pan()
  .activateAfterLongPress(200)
  .onUpdate((event) => {
    'worklet';
    translateY.value = event.translationY;
    // Calculate new position index
  })
  .onEnd(() => {
    'worklet';
    // Spring to final position
    translateY.value = withSpring(finalPosition);
    isActive.value = false;
  });

const composed = Gesture.Simultaneous(longPress, pan);
```

---

## Part 3: Shared Element Transition

### Requirements

Implement a smooth shared element transition between a list screen and a detail screen:

1. **Image morphing** — A thumbnail in the list smoothly expands into the detail header image
2. **Text transition** — Title text animates from list position to detail position
3. **Background fade** — Detail background fades in during transition
4. **Gesture-driven dismiss** — Swipe down on the detail screen to reverse the transition and dismiss
5. **Interruptible** — The transition can be interrupted mid-animation by a gesture

### Visual Specification

```
  List Screen                    Detail Screen
  ┌──────────────┐              ┌──────────────┐
  │ ┌──┐ Title 1 │              │              │
  │ │  │ desc    │              │   ┌──────┐   │
  │ └──┘         │   ─ tap ──▶  │   │      │   │
  │ ┌──┐ Title 2 │              │   │ img  │   │
  │ │  │ desc    │              │   │      │   │
  │ └──┘         │              │   └──────┘   │
  │              │              │              │
  │              │              │  Title 1     │
  │              │              │  description │
  └──────────────┘              └──────────────┘
                                  ↕ swipe to dismiss
```

---

## Test Criteria

1. **Swipe Card**: Cards follow gesture, rotate proportionally, snap correctly, spring back under threshold
2. **Drag Reorder**: Long press activates drag, items reorder correctly, spring animation on drop
3. **Shared Transition**: Image morphs smoothly, dismissible by gesture, transition is interruptible
4. **UI Thread**: All animations must run without JS thread callbacks (verify with `console.log` in worklets vs `runOnJS`)
5. **Spring Physics**: At least two animations use `withSpring` with custom damping/stiffness
6. **60 FPS**: No frame drops during any interaction (verify with Performance Monitor)

## Evaluation

```bash
make test
```
