# Concepts

- pending message는 local UI state가 아니라 sync 대상 record다.
- ack reconcile과 replay dedupe는 같은 identity rule을 공유한다.
- typing/presence는 durable record보다 ephemeral state에 가깝다.
