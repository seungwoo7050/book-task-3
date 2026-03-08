# Attack Lab Docs

## Purpose

This folder keeps the public explanation for the migrated Attack Lab project.

It explains:

- what the official lab is trying to teach
- what the companion verifier does and does not claim
- what can safely be published in a public study repository

## Document Map

- [`concepts/payload-models.md`](concepts/payload-models.md): the five phase families and their byte-level invariants
- [`concepts/rop-and-relative-addressing.md`](concepts/rop-and-relative-addressing.md): why code injection and ROP require different reasoning
- [`references/publication-policy.md`](references/publication-policy.md): disclosure boundary for exploit-related material
- [`references/verification.md`](references/verification.md): commands and current results for both the public self-study targets and the companion tracks

## Disclosure Policy

- explain stack-layout and payload reasoning
- explain why defenses change the payload model
- publish the verified payload files for the public `target1` self-study instance
- do not publish raw exploit strings for private or course-issued targets
