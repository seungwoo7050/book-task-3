# ROP And Relative Addressing

## Code Injection vs ROP

The main conceptual split in Attack Lab is this:

- On `ctarget`, the stack is executable, so the attacker can redirect control into injected bytes.
- On `rtarget`, the stack is not executable and the stack address changes, so the attacker must
  reuse existing code snippets and compute addresses relative to the current stack.

## Why Phase 5 Is Different

Phase 5 is harder because it combines two constraints:

- the cookie string still has to exist somewhere in the payload
- its absolute stack address is not stable

So the payload has to:

1. capture a live stack pointer
2. add a known offset to reach the string
3. move the computed address into the first argument register
4. return into the target function

That "address as data" transition is the core lesson of the final phase.
