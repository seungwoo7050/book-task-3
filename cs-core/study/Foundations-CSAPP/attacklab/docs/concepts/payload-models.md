# Payload Models

## Why A Companion Verifier Exists

The official Attack Lab is centered on exploiting externally supplied binaries. Those binaries are
missing in the legacy tree and should not be blindly committed into a public repository.

The study migration therefore adds a second layer: a verifier that checks whether a hex payload
matches the intended exploit structure for each phase.

## Phase Families

| Phase | Official idea | Companion invariant |
|---|---|---|
| 1 | overwrite return address to `touch1` | 40-byte frame fill plus `touch1` return slot |
| 2 | code injection to call `touch2(cookie)` | shellcode prefix plus return-to-buffer |
| 3 | code injection to call `touch3(cookie_string)` | shellcode prefix plus safe cookie-string placement |
| 4 | ROP to call `touch2(cookie)` | `pop -> mov -> touch2` gadget chain |
| 5 | ROP to call `touch3(cookie_string)` | `%rsp` capture, relative offset, address computation, then `touch3` |

## What The Companion Verifier Preserves

- little-endian address encoding
- stack-frame size reasoning
- cookie handling
- distinction between code injection and ROP
- runtime-relative addressing in the final phase

## What It Does Not Claim

- It is not the official lab target.
- It does not execute attacker-supplied machine code.
- Passing companion verification does not prove a payload would pass against a real supplied
  `ctarget` or `rtarget`.
