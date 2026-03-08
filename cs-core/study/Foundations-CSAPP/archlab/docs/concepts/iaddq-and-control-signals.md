# iaddq And Control Signals

## Core Lesson

The most important insight in Part B is that "add one instruction" does not mean "change one line."

`iaddq V, rB` touches:

- fetch shape, because it carries both regids and an immediate
- decode selection, because it reads `rB`
- ALU input routing, because it combines `valB` and `valC`
- condition-code update, because it behaves like an arithmetic instruction
- write-back destination, because the result returns to `rB`

## Companion Model Boundary

The companion project does not parse HCL. Instead, it models the semantic outcome that HCL is
supposed to produce:

- `next_pc = pc + 10`
- `valE = valB + valC`
- `dstE = rB`
- `ZF`, `SF`, and `OF` derived from the result

This keeps the control-signal reasoning visible and testable.
