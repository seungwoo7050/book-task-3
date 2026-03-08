# Publication Policy

## Purpose

Bomb Lab sits close to two boundaries:

- course-asset redistribution
- turning a study repository into a spoiler dump

This project uses the following rules.

## Allowed In Public

- the official problem contract without the actual binary
- helper scripts that operate on a locally supplied binary
- workflow notes for `gdb`, `objdump`, `strings`, and `nm`
- generic explanations of phase families
- the verified answer file for the public CMU self-study bomb
- fresh companion implementations written for this repository
- tests and verification logs for the companion implementations

## Not Allowed In Public

- the official `code/bomb` executable
- raw solution strings for a supplied private or course-specific bomb
- large disassembly dumps copied into public docs
- writeups that are only answer keys and not learning artifacts

## Local-Only Material

If the user later obtains a private or course-issued bomb locally, the following should stay
outside public Git history:

- the binary itself
- exact answers for that binary
- raw dumps generated directly from that binary unless there is a clear rights basis

The `notion/` tree may discuss workflow and reasoning, but it should still avoid becoming a public
answer key for a specific externally supplied bomb.
