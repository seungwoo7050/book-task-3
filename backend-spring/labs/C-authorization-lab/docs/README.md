# C-authorization-lab Notes

## Implemented now

- organization creation
- invite issue and accept flow
- role change endpoint

## Important simplifications

- authorization rules are represented through service logic, not Spring method security yet
- membership state is held in memory
- ownership checks are explained by API shape, not by a full policy engine

## Next improvements

- move role checks into Spring Security method annotations
- persist memberships and invitations
- add forbidden-path tests that prove denied access behavior
